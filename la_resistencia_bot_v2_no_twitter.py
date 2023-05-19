import os
import requests
import time

import speech_recognition as sr
from pydub import AudioSegment
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from webdriver_manager.chrome import ChromeDriverManager

from CONF import SG_token
from CONF import _email
from CONF import _email_j
from CONF import _email_s

delayTime = 2
audioToTextDelay = 10
filename = '1.mp3'
byPassUrl = 'https://publico.elterrat.com/programa/la-resistencia/formulario/'
googleIBMLink = 'https://speech-to-text-demo.ng.bluemix.net/'

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument("--mute-audio")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def audioToText(mp3Path):
    driver.execute_script('''window.open("","_blank");''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(googleIBMLink)
    delayTime = 10
    # Upload file
    time.sleep(1)
    # Upload file
    time.sleep(1)
    root = driver.find_element(By.ID, 'root').find_elements(By.CLASS_NAME, 'dropzone _container _container_large')
    btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    btn.send_keys(mp3Path)
    # Audio to text is processing
    time.sleep(delayTime)
    # btn.send_keys(path)
    # Audio to text is processing
    time.sleep(audioToTextDelay)
    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div').find_elements(By.TAG_NAME, 'span')
    result = " ".join([each.text for each in text])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return result


def saveFile(content, filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)


def check_table(slot_available):
    datepicker_table = driver.find_elements(By.CLASS_NAME, 'ui-datepicker-calendar')[0]
    for row in datepicker_table.find_elements(By.CSS_SELECTOR, 'tr'):
        for cell in row.find_elements(By.CSS_SELECTOR, 'td'):
            if "unselectable" not in (cell.get_attribute('class')):
                slot_available = True
            else:
                print(f'{cell.text} is full or invalid')
    return slot_available


def send_email():
    print('sending message')
    message = Mail(
        from_email=_email,
        to_emails=_email,
        subject='La resistencia BOT',
        html_content='<strong>HOLA ENTRADES DISPONIBLES ILLO!</strong>')
    try:
        sg = SendGridAPIClient(SG_token)
        response = sg.send(message)
    except Exception as e:
        print(e.message)

    print('sending message')
    message = Mail(
        from_email=_email,
        to_emails=_email_j,
        subject='La resistencia BOT',
        html_content='<strong>HOLA ENTRADES DISPONIBLES ILLO!</strong>')
    try:
        sg = SendGridAPIClient(SG_token)
        response = sg.send(message)
    except Exception as e:
        print(e.message)

    print('sending message')
    message = Mail(
        from_email=_email,
        to_emails=_email_s,
        subject='La resistencia BOT',
        html_content='<strong>HOLA ENTRADES DISPONIBLES ILLO!</strong>')
    try:
        sg = SendGridAPIClient(SG_token)
        response = sg.send(message)
    except Exception as e:
        print(e.message)


driver.get(byPassUrl)
time.sleep(1)
recaptcha_done_flag = False

if len(driver.find_elements(By.CLASS_NAME, 'g-recaptcha')) <= 0:
    recaptcha_done_flag = True
else:
    googleClass = driver.find_elements(By.CLASS_NAME, 'g-recaptcha')[0]
    time.sleep(2)
    outeriframe = googleClass.find_element(By.TAG_NAME, 'iframe')
    time.sleep(2)
    outeriframe.click()
    time.sleep(2)
    siguiente_btn = driver.find_element(By.CSS_SELECTOR, ".button")
    try:
        siguiente_btn.click()
        recaptcha_done_flag = True
    except WebDriverException:

        time.sleep(2)
        allIframesLen = driver.find_elements(By.TAG_NAME, 'iframe')
        time.sleep(1)
        audioBtnFound = False

        audioBtnIndex = -1
        for index in range(len(allIframesLen)):
            driver.switch_to.default_content()
            iframe = driver.find_elements(By.TAG_NAME, 'iframe')[index]
            driver.switch_to.frame(iframe)
            driver.implicitly_wait(delayTime)
            try:
                audioBtn = driver.find_element(By.ID, 'recaptcha-audio-button') or driver.find_element(By.ID,
                                                                                                       'recaptcha-anchor')
                audioBtn.click()
                audioBtnFound = True
                audioBtnIndex = index
                break
            except Exception as e:
                pass
        if audioBtnFound:
            try:
                while True:
                    href = driver.find_element(By.ID, 'audio-source').get_attribute('src')
                    response = requests.get(href, stream=True)
                    saveFile(response, filename)
                    # response = audioToText(os.getcwd() + '/' + filename)
                    # convert wav to mp3
                    dst = "1.wav"
                    sound = AudioSegment.from_mp3(filename)
                    sound.export(dst, format="wav")
                    r = sr.Recognizer()
                    with sr.AudioFile(dst) as source:
                        audio_data = r.record(source)
                        response = r.recognize_google(audio_data)

                    driver.switch_to.default_content()
                    iframe = driver.find_elements(By.TAG_NAME, 'iframe')[audioBtnIndex]
                    driver.switch_to.frame(iframe)
                    inputbtn = driver.find_element(By.ID, 'audio-response')
                    inputbtn.send_keys(response)
                    inputbtn.send_keys(Keys.ENTER)
                    time.sleep(2)
                    errorMsg = driver.find_elements(By.CLASS_NAME, 'rc-audiochallenge-error-message')[0]
                    if errorMsg.text == "" or errorMsg.value_of_css_property('display') == 'none':
                        time.sleep(2)
                        driver.switch_to.default_content()
                        siguiente_btn = driver.find_element(By.CSS_SELECTOR, ".button")
                        time.sleep(3)
                        siguiente_btn.click()
                        time.sleep(2)
                        recaptcha_done_flag = True
                        break
            except Exception as e:
                print(e)
                print('Caught. Need to change proxy now')
        else:
            print('Button not found. This should not happen.')

    if recaptcha_done_flag == True:
        slot_available = False

        time.sleep(1)
        input_date_field = driver.find_element(By.XPATH,
                                               "//li[@class='gfield gfield--type-date gfield--input-type-datepicker gfield--datepicker-no-icon limitar_fecha always field_sublabel_below gfield--no-description field_description_below gfield_visibility_visible gf_repeater2_child_field']")
        input_date_field.click()
        time.sleep(1)
        slot_available = check_table(slot_available)
        time.sleep(1)

        try:
            get_next = driver.find_element(By.XPATH, "//a[@class='ui-datepicker-next ui-corner-all']")
            time.sleep(2)
            get_next.click()
            slot_available = check_table(slot_available)
        except:
            print('next is disabled.')

        try:
            get_prev = driver.find_element(By.XPATH, "//a[@class='ui-datepicker-prev ui-corner-all']")
            time.sleep(2)
            get_prev.click()
            slot_available = check_table(slot_available)
        except:
            print('prev is disabled.')

        if slot_available:
            send_email()
            print('email sent!')
        else:
            print('Script run successfully but no slots available.')
