from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class AuthPage(BasePage):
    URL = 'https://b2c.passport.rt.ru/'

    # Локаторы элементов
    COOKIES_BUTTON = (By.XPATH, '//*[@id="cookies-tip-open"]') # Кнопка для открытия модального окна Cookie
    COOKIES_WINDOW = (By.CSS_SELECTOR, '.rt-tooltip') # Модальное окно Cookie
    COOKIES_CLOSE_X = (By.CSS_SELECTOR, '.rt-tooltip__close') # Кнопка "х" для закрытия модального окна Cookie
    TAB_PHONE = (By.ID, 't-btn-tab-phone') # Таб "Телефон"
    TAB_EMAIL = (By.ID, 't-btn-tab-mail') # Таб "Почта"
    TAB_LOGIN = (By.ID, 't-btn-tab-login') # Таб "Логин"
    TAB_LS = (By.ID, 't-btn-tab-ls') # Таб "Лицевой счёт"
    INPUT_USERNAME = (By.ID, 'username') # Поле ввода логина
    INPUT_PASSWORD = (By.ID, 'password') # Поле ввода пароля
    SECTION_PROMO = (By.ID, 'page-left') # Секция с логотипом и описанием
    SECTION_RIGHT = (By.ID, 'page-right')  # Основная секция (правая)
    PROMO_TITLE = (By.CSS_SELECTOR, '.what-is__title') # Заголовок "Личный кабинет"
    PROMO_DESC = (By.CSS_SELECTOR, '.what-is__desc') # Описание "Персональный помощник..."
    INPUT_MASK = (By.CSS_SELECTOR, '.rt-input__mask') # Общий контейнер маски ввода телефона
    INPUT_MASK_START = (By.CSS_SELECTOR, '.rt-input__mask-start') # Стартовая часть маски, где отображается "+7"
    BUTTON_LOGIN = (By.ID, 'kc-login') # Кнопка "Войти"
    ERROR_MESSAGE = (By.ID, 'form-error-message') # Сообщения с ошибками
    FORGOT_PASSWORD_LINK = (By.ID, 'forgot_password') # Кнопка-ссылка "Забыл пароль"
    FIELD_ERROR_MESSAGE = (By.ID, 'username-meta')  # Ошибка валидации под полем ввода логина
    AGREEMENT_LINK = (By.ID, 'rt-auth-agreement-link') # Кнопка-ссылка "Пользовательское соглашение"

    def is_cookies_window_present(self, visible: bool = True):
        """Проверяет, присутствует ли окно Cookie видно (visible=True) или скрыто (visible=False), с ожиданием соответствующего состояния."""
        if visible:
            return self.wait.until(EC.visibility_of_element_located(self.COOKIES_WINDOW)).is_displayed()
        else:
            return self.wait.until(EC.invisibility_of_element_located(self.COOKIES_WINDOW))

    def is_form_split_into_two_blocks(self):
        """Проверить, что форма визуально разделена на два блока (оба отображаются)."""
        left_block = self.wait.until(EC.visibility_of_element_located(self.SECTION_PROMO))
        right_block = self.wait.until(EC.visibility_of_element_located(self.SECTION_RIGHT))
        # Проверяем базовое условие, что оба блока присутствуют и видны
        if left_block.is_displayed() and right_block.is_displayed():
            # Дополнительная проверка: левый блок должен находиться левее правого по координате X
            return left_block.location['x'] < right_block.location['x']
        return False

    def enter_username(self, text):
        """Ввести текст в универсальное поле ввода."""
        self.clear_field(self.INPUT_USERNAME)  # Используем базовый метод очистки
        element = self.wait.until(EC.visibility_of_element_located(self.INPUT_USERNAME))
        element.send_keys(text)
        element.send_keys(Keys.ENTER)

    def is_phone_mask_visible(self):
        """Проверить, что маска телефона появилась на экране."""
        try:
            return self.wait.until(EC.visibility_of_element_located(self.INPUT_MASK)).is_displayed()
        except Exception:
            return False

    def get_username_input_value(self):
        """Получить текущее текстовое значение из поля ввода логина."""
        element = self.wait.until(EC.visibility_of_element_located(self.INPUT_USERNAME))
        return element.get_attribute('value')

    def append_character_to_username(self, char):
        """Дописать один символ в конец поля ввода без очистки поля."""
        element = self.wait.until(EC.visibility_of_element_located(self.INPUT_USERNAME))
        element.send_keys(char)

    def enter_password(self, text):
        """Ввести текст в универсальное поле ввода."""
        self.clear_field(self.INPUT_PASSWORD)  # Используем базовый метод очистки
        element = self.wait.until(EC.visibility_of_element_located(self.INPUT_PASSWORD))
        element.send_keys(text)

    def get_forgot_password_color(self):
        """Получить цвет текстового элемента 'Забыл пароль' в формате RGBA/HEX."""
        element = self.wait.until(EC.visibility_of_element_located(self.FORGOT_PASSWORD_LINK))
        return element.value_of_css_property('color')

    def switch_to_new_tab(self):
        """Ожидает открытия новой вкладки и переключает на нее фокус WebDriver."""
        # Динамическое ожидание: ждем, пока количество вкладок (handles) станет больше 1
        self.wait.until(lambda driver: len(driver.window_handles) > 1)
        # Получаем список всех вкладок
        handles = self.driver.window_handles
        # Переключаемся на самую последнюю (новую) вкладку в списке
        self.driver.switch_to.window(handles[-1])