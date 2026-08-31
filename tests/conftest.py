import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.auth_page import AuthPage
from pages.reg_page import RegPage


@pytest.fixture
def driver():
    """Чистый Selenium с маскировкой от WAF через CDP."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Отключаем явные маркеры автоматизации
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # Отключаем Blink-фичи автоматизации
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    # Подменяем navigator.webdriver на undefined в JS до загрузки страницы
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    yield driver
    driver.quit()

@pytest.fixture
def auth_page(driver):
    """Фикстура для автоматической подготовки страницы авторизации перед каждым тестом."""
    page = AuthPage(driver)
    page.maximize_window()
    page.open(page.URL)
    return page

@pytest.fixture
def reg_page(driver):
    """Фикстура для автоматической подготовки страницы авторизации перед каждым тестом."""
    page = RegPage(driver)
    page.maximize_window()
    page.open(page.URL)
    page.click_locator((By.ID, 'kc-register'))
    return page
