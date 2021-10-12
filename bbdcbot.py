from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime as dt
from dateutil import relativedelta as rd
import time

# User inputs
PATH = input("Path of chromedriver (eg C:\Program Files (x86)\chromedriver.exe): ")
username = input("Username: ")
password = input("Password: ")

def bbdc_bot():
    driver = webdriver.Chrome(PATH)
    driver.get("https://info.bbdc.sg/members-login/")
    # Login page
    try:
        usernamebox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtNRIC")))
        usernamebox.send_keys(username)
        passwordbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtPassword")))
        passwordbox.send_keys(password)
        login = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "loginbtn")))
        login.click()
    except Exception as e:
        print(e)
        print("Error at login")
        driver.quit()
    # Information not secure page
    try:
        proceed = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "proceed-button")))
        proceed.click()
        print("Login successful")
    except Exception as e:
        print(e)
        print("Error at secure page")
        driver.quit()
    # Home page
    try:
        # click TP simulator booking
        driver.switch_to.frame("leftFrame")
        booking = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Booking")))
        booking.click()
        # click module 1 and submit
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_name('mainFrame')))
        optin = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "optTest")))
        optin.click()
        submit = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "btnSubmit")))
        submit.click()
    except Exception as e:
        print(e)
        print("Error at home page")
        driver.quit()
    # Month, session and day selector
    try:
        months = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "allMonth")))
        months.click()
        sessions = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "allSes")))
        sessions.click()
        days = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "allDay")))
        days.click()
        search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "btnSearch")))
        search.click()
    except Exception as e:
        print(e)
        print("Error when selecting month, session and day")
        driver.quit()
    # Available slots
    try:
        # finding first available slot and checking if it is within one month
        firstslot = WebDriverWait(driver, 180).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/table/tbody/tr/td[2]/form/table[1]/tbody/tr[9]/td/table/tbody/tr[3]/td[1]")))
        firstslot = firstslot.text[:6] + firstslot.text[8:10]
        firstslot = dt.datetime.strptime(firstslot, "%d/%m/%y")
        onemonth = dt.datetime.now() + rd.relativedelta(months=1)
        if firstslot < onemonth:
            # book earliest available slot if it is within one month
            sessionbutton = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "slot")))
            sessionbutton.click()
            submitbutton = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/table/tbody/tr/td[2]/form/table[2]/tbody/tr[1]/td[1]/input[2]")))
            submitbutton.click()
            confirmbutton = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/table/tbody/tr/td[2]/form/table/tbody/tr[14]/td[2]/input[2]")))
            confirmbutton.click()
            date = firstslot.strftime(("%d/%m/%y"))
            print("Available slot within one month. Slot booked. Slot date:", date)
            booked = 1
            time.sleep(5)
            driver.quit()
        else:
            date = firstslot.strftime(("%d/%m/%y"))
            print("Earliest slot is not within one month. Earliest date:", date)
            now = dt.datetime.now()
            currenttime = now.strftime("%d/%m/%y %H:%M")
            print("Last check:", currenttime)
            driver.quit()
    except Exception as e:
        print(e)
        print("Error when finding available slot")
        driver.quit()

booked = 0
while booked == 0:
    bbdc_bot()
    time.sleep(600)