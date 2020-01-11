from selenium.webdriver.common.by import By


class AcListPageLocators:
    AC_NO = 0
    """A class for main page locators. All main page locators should come here"""
    CONSTITUENCY_HYPERLINK = ()

    @classmethod
    def set_ac_no(cls, ac_no):
        cls.AC_NO = ac_no
        cls.CONSTITUENCY_HYPERLINK = (By.XPATH, f'//*[@id="main-content"]/div/div[2]/div/div[{cls.AC_NO}]/a')


class BoothListPageLocators:

    BOOTH_NO = 0
    BOOTH_NUMBER_HYPERLINK = ()
    BOOTH_DIV = (By.XPATH, '//*[@id="main-content"]/div/div[2]/div/div')

    @classmethod
    def set_booth_no(cls, booth_no):
        cls.BOOTH_NO = booth_no
        cls.BOOTH_NUMBER_HYPERLINK = (By.XPATH,
                                      f'//*[@id="main-content"]/div/div[2]/div/div[{cls.BOOTH_NO + 1}]/div[2]/a')


class CaptchaPageLocators:

    CAPTCHA_IMAGE = (By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_myImage"]')
    NEXT_BUTTON = (By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_ButtonSearchApplicationStatus"]')
    CAPTCHA_REQUIRED_STAR = (By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_rfvServiceIdTokenNo0"]')


class ServerErrorPageLocators:
    SERVER_ERROR_TEXT = "Server Error in '/' Application"
