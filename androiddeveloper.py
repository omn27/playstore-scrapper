from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import os
import time


def checkAccountExistsAndroidDeveloper(email):
    binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
    profile = FirefoxProfile(
        "C:\\Users\\Octavio\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\4raoxbzz.default-release"
    )
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.socks", "127.0.0.1")
    profile.set_preference("network.proxy.socks_port", 9050)
    driver = webdriver.Firefox(
        firefox_profile=profile,
        firefox_binary=binary,
        executable_path="C:\\Users\\Octavio\\AppData\\Local\\Programs\\Python\\Python39\\geckodriver.exe",
    )
    driver.get(
        "https://developer.android.com/_d/signin?continue=https%3A%2F%2Fdeveloper.android.com%2F&prompt=select_account"
    )

    email_field = driver.find_element_by_xpath('//*[@id="identifierId"]')
    email_field.send_keys(email)

    dom_button = driver.find_element_by_xpath(
        '//*[@id="identifierNext"]/div/button/div[2]'
    )
    dom_button.click()

    text = "Inténtalo con un navegador diferente. Si usas un navegador compatible, actualiza la página y accede de nuevo."
    time.sleep(6)
    if text in driver.page_source:
        driver.quit()
        return True
    driver.quit()
    return False
