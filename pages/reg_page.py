from telnetlib import EC
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class RegPage(BasePage):
    URL = 'https://b2c.passport.rt.ru/'

    # Локаторы элементов
    INPUT_FIRSTNAME = (By.CSS_SELECTOR, "input[name='firstName']") # Поля ввода "Имя"
    FIRSTNAME_ERROR = (By.XPATH, "//input[@name='firstName']/following-sibling::span[contains(@class, 'meta--error')] | //input[@name='firstName']/../../span[contains(@class, 'meta--error')]") # Ошибка для поля ввода "Имя"
    INPUT_LASTNAME = (By.CSS_SELECTOR, "input[name='lastName']") # Поле ввода "Фамилия"
    LASTNAME_ERROR = (By.XPATH, "//input[@name='lastName']/../../span[contains(@class, 'meta--error')]") # Ошибка для поля ввода "Фамилия"
    REGION_INPUT = (By.CSS_SELECTOR, 'input.rt-select__input') # Поле выбора "Регион"
    INPUT_ADDRESS = (By.ID, 'address') # Поле ввода "E-mail или мобильный телефон"
    ADDRESS_ERROR = (By.XPATH, "//input[@id='address']/../../following-sibling::span[contains(@class, 'meta--error')] | //input[@id='address']/../following-sibling::span[contains(@class, 'meta--error')]") # Ошибка для поля ввода "E-mail или мобильный телефон"
    INPUT_PASSWORD = (By.ID, 'password') # Поле для ввода "Пароль"
    PASSWORD_ERROR = (By.XPATH, "//input[@id='password']/../../span[contains(@class, 'meta--error')]") # Ошибка для поля ввода "Пароль"
    INPUT_PASSWORD_CONFIRM = (By.ID, 'password-confirm') # Поле ввода "Подтверждение пароля"
    PASSWORD_CONFIRM_ERROR = (By.XPATH, "//input[@id='password-confirm']/../../span[contains(@class, 'meta--error')]") # Ошибка для поля ввода "Подтверждение пароля"

    def get_default_region_value(self):
        """Получить текущее значение (атрибут value) из поля 'Регион'."""
        element = self.driver.find_element(*self.REGION_INPUT)
        return element.get_attribute('value')








