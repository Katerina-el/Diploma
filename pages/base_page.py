from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        self.driver.get(url)

    def click_locator(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def maximize_window(self):
        """Развернуть окно браузера на весь экран."""
        self.driver.maximize_window()

    def clear_field(self, locator):
        """Полностью очистить поле."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)
        element.clear()

    def get_element_text(self, locator: tuple) -> str:
        """Возвращает текст видимого элемента, найденного по локатору."""
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def enter(self, locator, text, submit=False):
        """Ввести текст в универсальное поле ввода с опциональным нажатием Enter."""
        self.clear_field(locator)  # Используем базовый метод очистки
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.send_keys(text)
        # Если при вызове передали submit=True, то нажимаем Enter
        if submit:
            element.send_keys(Keys.ENTER)

    def is_tab_active(self, locator):
        """Проверить, что таб активен."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return 'rt-tab--active' in element.get_attribute('class')

    def is_element_visible(self, locator: tuple) -> bool:
        """Проверяет, виден ли элемент по локатору (с ожиданием появления)."""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except Exception:
            return False