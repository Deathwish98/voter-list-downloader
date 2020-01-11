from element import BasePageElement
from locators import AcListPageLocators, BoothListPageLocators, CaptchaPageLocators, ServerErrorPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
from captcha_resolver import CaptchaResolver
import os


class BasePage:
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver


class AcListPage(BasePage):

    # # Declares a variable that will contain the retrieved text
    # search_text_element = SearchTextElement()

    def click_ac_hyperlink(self, ac_no):
        AcListPageLocators.set_ac_no(ac_no)
        element = self.driver.find_element(*AcListPageLocators.CONSTITUENCY_HYPERLINK)
        element.click()


class BoothListPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.total_booths = 0
        self.find_total_no_of_booths()

    def find_total_no_of_booths(self):
        self.total_booths = len(self.driver.find_elements(*BoothListPageLocators.BOOTH_DIV)) - 1

    def click_booth_hyperlink(self, booth_no):
        BoothListPageLocators.set_booth_no(booth_no)
        element = self.driver.find_element(*BoothListPageLocators.BOOTH_NUMBER_HYPERLINK)
        element.click()


class CaptchaPage(BasePage):

    ctl00_ContentPlaceHolder1_TextBoxcaptacha = BasePageElement('ctl00_ContentPlaceHolder1_TextBoxcaptacha')

    CAPTCHA_PATH = 'captcha.png'

    def __init__(self, driver):
        super().__init__(driver)

    def download_captcha(self):
        # element = WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located(CaptchaPageLocators.CAPTCHA_IMAGE)
        # )

        self.driver.switch_to.window(self.driver.window_handles[1])

        element = self.driver.find_element(*CaptchaPageLocators.CAPTCHA_IMAGE)
        element.screenshot(CaptchaPage.CAPTCHA_PATH)

        # src = element.get_attribute('src')
        # urllib.request.urlretrieve(src, CaptchaPage.CAPTCHA_PATH)

    def resolve_captcha(self):
        captcha_resolver = CaptchaResolver(CaptchaPage.CAPTCHA_PATH)
        captcha_resolver.read_captcha()
        print(captcha_resolver.captcha_text)
        self.delete_captcha_file()
        return captcha_resolver.captcha_text

    def click_next_button(self):
        element = self.driver.find_element(*CaptchaPageLocators.NEXT_BUTTON)
        element.click()

    def no_captcha_entered(self):
        element = self.driver.find_element(*CaptchaPageLocators.CAPTCHA_REQUIRED_STAR)
        attribute_value = element.get_attribute("style")

        if 'visible' in attribute_value:
            return True

    def accept_alert_if_any(self):
        WebDriverWait(self.driver, 1).until(EC.alert_is_present(),
                                            'Timed out waiting for PA creation ' +
                                            'confirmation popup to appear.')

        alert = self.driver.switch_to.alert
        alert.accept()
        return True

    @staticmethod
    def delete_captcha_file():
        try:
            os.remove(CaptchaPage.CAPTCHA_PATH)
        except FileNotFoundError:
            print('File does not exist')


class ServerErrorPage(BasePage):

    def is_server_error(self):
        if ServerErrorPageLocators.SERVER_ERROR_TEXT in self.driver.page_source:
            return True
