import asyncio
import logging
import os

import telegram
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

load_dotenv()
URL = "https://agendamentosonline.mne.gov.pt/AgendamentosOnline/app/scheduleAppointmentForm.jsf"
SEARCH_TEXT = 'De momento não existem vagas disponíveis, por favor tente mais tarde.'


def start_webdriver(headless):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
        # Bypass OS security model
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/88.0.4324.150 Safari/537.36")
        chrome_options.add_argument('--window-size=1920,1080')
        # Additional options for Docker environment
        chrome_options.add_argument("--disable-gpu")  # This option is necessary for headless mode
        chrome_options.add_argument("--no-sandbox")  # This option bypasses OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("--remote-debugging-port=9222")  # This is important for Docker
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument('--disable-setuid-sandbox')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    return webdriver.Chrome(options=chrome_options,service=ChromeService(ChromeDriverManager().install()))


def appointment_is_available(browser_inst):
    try:
        # browser_inst.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        # Wait for the element to be clickable and then click it
        wait = WebDriverWait(browser_inst, 15)
        browser_inst.save_screenshot("screenshot.png")
        # Fill ID with keyboard input
        input_element = wait.until(EC.element_to_be_clickable((By.ID, "scheduleForm:tabViewId:ccnum")))
        # Fill the input element with the desired value
        input_element.send_keys(os.getenv("PASSPORT_ID"))
        # Wait for the date input element to be clickable
        date_input_element = wait.until(
            EC.element_to_be_clickable((By.ID, "scheduleForm:tabViewId:dataNascimento_input")))
        date_input_element.send_keys(os.getenv("PASSPORT_DATE"))
        # Fill the date input element
        search_button = wait.until(EC.element_to_be_clickable((By.ID, "scheduleForm:tabViewId:searchIcon")))
        search_button.click()
        # Press on the submit button
        search_button = wait.until(EC.element_to_be_clickable((By.ID, "scheduleForm:tabViewId:searchIcon")))
        search_button.click()
        # Wait for the specific option to be clickable and click it
        dropdown_trigger = wait.until(EC.element_to_be_clickable((By.ID, "scheduleForm:postcons_label")))
        dropdown_trigger.click()
        # Wait for the specific option to be visible and clickable
        option_xpath = "//li[contains(text(), 'Secção Consular da Embaixada de Portugal em Telavive')]"
        option_element = wait.until(EC.visibility_of_element_located((By.XPATH, option_xpath)))
        option_element.click()
        # Wait for the dropdown to be clickable and click it
        wait = WebDriverWait(browser_inst, 10)
        dropdown_trigger = wait.until(EC.element_to_be_clickable((By.ID, "scheduleForm:categato_label")))
        dropdown_trigger.click()
        # Wait for the specific option to be visible and clickable
        option_xpath = "//li[contains(., 'Documentos de identificação civil')]"
        option_element = wait.until(EC.visibility_of_element_located((By.XPATH, option_xpath)))
        option_element.click()
        # Click on submit button
        add_button = wait.until(EC.element_to_be_clickable((By.ID, "scheduleForm:bAddAto")))
        add_button.click()
        # Press on the checkbox
        checkbox = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".ui-chkbox-box.ui-widget.ui-corner-all.ui-state-default")))
        checkbox.click()
        # Press on the submit button
        calendarize_button = wait.until(EC.element_to_be_clickable((By.ID, "scheduleForm:dataTableListaAtos:0:bCal")))
        calendarize_button.click()
        text_xpath = f"//*[contains(text(), '{SEARCH_TEXT}')]"
        text_element = wait.until(EC.visibility_of_element_located((By.XPATH, text_xpath))).text
        # Read the text from the element

        return SEARCH_TEXT != text_element
    except Exception as e:
        logging.error(e)
        return True


async def send_telegram_message(message, token, chat_id):
    bot = telegram.Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message)


if __name__ == '__main__':
    try:
        browser = start_webdriver(headless=True)
        browser.get(URL)
        if appointment_is_available(browser):
            asyncio.run(
                send_telegram_message(f"Appointment is available! or something went wrong \n {URL}", os.getenv("TELEGRAM_TOKEN"),
                                      os.getenv("TELEGRAM_GROUP")))
        else:
            if os.getenv("INFORM_ON_MISSING", False):
                asyncio.run(send_telegram_message("No appointment available", os.getenv("TELEGRAM_TOKEN"),
                                                  os.getenv("TELEGRAM_GROUP")))
        browser.quit()
    except Exception as main_exception:
        logging.error(main_exception)

