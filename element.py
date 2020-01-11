from selenium.webdriver.support.ui import WebDriverWait


class BasePageElement:

    def __init__(self, locator):
        self.locator = locator

    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        driver = obj.__dict__.get('driver')
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element_by_id(self.locator))
        driver.find_element_by_id(self.locator).clear()
        driver.find_element_by_id(self.locator).send_keys(value)

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        driver = obj.__dict__.get('driver')
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element_by_id(self.locator))
        element = driver.find_element_by_id(self.locator)
        return element.get_attribute("value")
