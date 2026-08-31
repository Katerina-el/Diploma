def test_004_open_window_cookie(auth_page):
    """FOOT-004: Открытие информационного окна «Мы используем Cookie»"""
    auth_page.click_locator(auth_page.COOKIES_BUTTON)
    assert auth_page.is_cookies_window_present(visible=True), ("Информационное окно 'Мы используем Cookie' не появилось!")

def test_005_close_window_cookie(auth_page):
    """FOOT-005: Закрытие окна «Мы используем Cookie» нажатием на крестик «Х»"""
    auth_page.click_locator(auth_page.COOKIES_BUTTON)
    assert auth_page.is_cookies_window_present(visible=True), ("Информационное окно 'Мы используем Cookie' не появилось!")
    auth_page.click_locator(auth_page.COOKIES_CLOSE_X)
    assert auth_page.is_cookies_window_present(visible=False), ("Информационное окно 'Мы используем Cookie' не закрылось!")

