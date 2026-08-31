import time
import test_data

def test_001_default_state_auth_form(auth_page):
    """FAU-001: Дефолтное состояние формы «Авторизация»"""
    assert auth_page.is_form_split_into_two_blocks(), "Форма НЕ разделена вертикально на два блока (один из блоков скрыт или они перекрывают друг друга)!"
    assert auth_page.get_element_text(auth_page.TAB_PHONE) == "Номер", "Таб 'Номер' не найден или текст некорректен"
    assert auth_page.get_element_text(auth_page.TAB_EMAIL) == "Почта", "Таб 'Почта' не найден или текст некорректен"
    assert auth_page.get_element_text(auth_page.TAB_LOGIN) == "Логин", "Таб 'Логин' не найден или текст некорректен"
    assert auth_page.get_element_text(auth_page.TAB_LS) == "Лицевой счёт" or "Лицевой счет", "Таб 'Лицевой счет' не найден или текст некорректен"
    assert auth_page.is_element_visible(auth_page.INPUT_USERNAME), "Поле ввода логина не отображается!"
    assert auth_page.is_element_visible(auth_page.INPUT_PASSWORD), "Поле ввода пароля не отображается!"
    assert auth_page.is_tab_active(auth_page.TAB_PHONE), "Таб 'Номер' должен быть активен по умолчанию!"
    assert auth_page.get_element_text(auth_page.PROMO_TITLE) == "Личный кабинет", "Заголовок промо-блока изменен или не отображается!"
    expected_desc = "Персональный помощник в цифровом мире Ростелекома"
    assert auth_page.get_element_text(auth_page.PROMO_DESC) == expected_desc, "Вспомогательный текст слогана не совпадает с ОР!"

def test_003_from_email_to_phone(auth_page):
    """FAU-003: Переключение с Почты на Телефон при полном вводе"""
    # ЧАСТЬ 1: Проверка ввода номера формата +79991112233
    auth_page.click_locator(auth_page.TAB_EMAIL)
    assert auth_page.is_tab_active(auth_page.TAB_EMAIL), "Не удалось переключиться на вкладку 'Почта' перед тестом +7!"
    phone_with_plus = "+79991112233"
    auth_page.enter(auth_page.INPUT_USERNAME, phone_with_plus, submit=True)
    assert auth_page.is_tab_active(auth_page.TAB_PHONE), (
        f"После ввода номера '{phone_with_plus}' во вкладке 'Почта', "
        f"автопереключение на вкладку 'Телефон' НЕ произошло!"
    )
    # ЧАСТЬ 2: Проверка ввода номера формата 89991112233
    auth_page.click_locator(auth_page.TAB_EMAIL)
    assert auth_page.is_tab_active(auth_page.TAB_EMAIL), "Не удалось вернуться на вкладку 'Почта' перед тестом с 8!"
    phone_with_eight = "89991112233"
    auth_page.enter(auth_page.INPUT_USERNAME, phone_with_eight, submit=True)
    assert auth_page.is_tab_active(auth_page.TAB_PHONE), (
        f"После ввода номера '{phone_with_eight}' во вкладке 'Почта' "
        f"автопереключение на вкладку 'Телефон' НЕ произошло!"
    )

def test_008_from_phone_to_email_correct(auth_page):
    """FAU-008: Переключение с Телефона на Почту при полном вводе"""
    auth_page.click_locator(auth_page.TAB_PHONE)
    assert auth_page.is_tab_active(auth_page.TAB_PHONE), "Не удалось переключиться на вкладку 'Почта'!"
    email_text = "user@mail.ru"
    auth_page.enter(auth_page.INPUT_USERNAME, email_text, submit=True)
    assert auth_page.is_tab_active(auth_page.TAB_EMAIL), (
        f"После ввода почты '{email_text}' во вкладке 'Телефон', "
        f"автопереключение на вкладку 'Почта' НЕ произошло!"
    )

def test_025_phone_mask_with_7(auth_page):
    """FAU-025: Активация маски телефона при вводе первой цифры «7»"""
    auth_page.click_locator(auth_page.TAB_PHONE)
    assert auth_page.is_tab_active(auth_page.TAB_PHONE), "Не удалось переключиться на вкладку 'Телефон'!"
    auth_page.enter(auth_page.INPUT_USERNAME, "7", submit=True)
    assert auth_page.is_phone_mask_visible(), "Маска телефона не появилась после ввода цифры '7'!"
    assert auth_page.get_element_text(auth_page.INPUT_MASK_START) == "+7", (
        f"Ожидалось начало маски '+7', но отображается '{auth_page.get_element_text(auth_page.INPUT_MASK_START)}'"
    )

def test_029_phone_len_limit(auth_page):
    """FAU-029: Ограничение длины ввода при включенной маске телефона"""
    auth_page.click_locator(auth_page.TAB_PHONE)
    assert auth_page.is_tab_active(auth_page.TAB_PHONE), "Не удалось переключиться на вкладку 'Телефон'!"
    valid_phone = "9123456789"
    auth_page.enter(auth_page.INPUT_USERNAME, valid_phone)
    # Так как маска форматирует вывод, в value может лежать как чистая строка, так и форматированная.
    # Проверяем, что введенные цифры присутствуют в поле
    value_after_step_1 = auth_page.get_username_input_value()
    # Удаляем из результата все нецифровые символы для сверки чистой длины
    digits_only_1 = "".join(filter(str.isdigit, value_after_step_1))
    assert len(digits_only_1) == 11, f"Ожидалось 11 цифр в поле, но получено {len(digits_only_1)} (Значение: {value_after_step_1})"
    # Попробовать ввести с клавиатуры еще одну любую цифру (12-ю по счету, например, 5)
    auth_page.append_character_to_username("5")
    # Ввод блокируется — 12-я цифра не появляется в поле, финальное значение не меняется
    value_after_step_2 = auth_page.get_username_input_value()
    digits_only_2 = "".join(filter(str.isdigit, value_after_step_2))
    assert len(digits_only_2) == 11, (
        f"Поле пропустило 12-ю цифру! "
        f"Длина строки: {len(digits_only_2)} цифр. Текущее значение: {value_after_step_2}"
    )
    assert "5" not in value_after_step_2[-1], "Лишняя цифра '5' добавилась в конец поля ввода!"

def test_033_login_incorrect_password(auth_page):
    """FAU-033: Ввод неверного пароля при зарегистрированном номере"""
    auth_page.click_locator(auth_page.TAB_PHONE)
    assert auth_page.is_tab_active(auth_page.TAB_PHONE), "Не удалось переключиться на вкладку 'Телефон'!"
    registered_phone = test_data.registered_phone # Необходим реальный телефон, который уже автоматизирован в системе
    auth_page.enter(auth_page.INPUT_USERNAME, registered_phone)
    auth_page.enter(auth_page.INPUT_PASSWORD, "WrongPassword123")
    auth_page.click_locator(auth_page.BUTTON_LOGIN)
    expected_error = "Неверный логин или пароль"
    actual_error = auth_page.get_element_text(auth_page.ERROR_MESSAGE)
    assert expected_error in actual_error, f"Ожидалась ошибка '{expected_error}', но получено: '{actual_error}'"
    actual_color = auth_page.get_forgot_password_color()
    expected_color = "rgba(255, 79, 18, 1)"
    assert expected_color in actual_color, (
        f"Элемент 'Забыл пароль' не перекрасился в нужный оранжевый цвет! "
        f"Ожидалось: '{expected_color}', но получено: '{actual_color}'"
    )

def test_041_login_unregistered_email(auth_page):
    """FAU-041: Ввод незарегистрированного email"""
    auth_page.click_locator(auth_page.TAB_EMAIL)
    assert auth_page.is_tab_active(auth_page.TAB_EMAIL), "Не удалось переключиться на вкладку 'Почта'!"
    # Генерируем заведомо несуществующий email (например, с текущим таймстампом)
    unregistered_email = f"user_not_exist_{int(time.time())}@qa-test-mail.com"
    auth_page.enter(auth_page.INPUT_USERNAME, unregistered_email)
    auth_page.enter(auth_page.INPUT_PASSWORD, "AnyPassword123!")
    auth_page.click_locator(auth_page.BUTTON_LOGIN)
    expected_error = "Неверный логин или пароль"
    actual_error = auth_page.get_element_text(auth_page.ERROR_MESSAGE)
    assert expected_error in actual_error, f"Ожидалась ошибка '{expected_error}', но получено: '{actual_error}'"
    actual_color = auth_page.get_forgot_password_color()
    expected_color = "rgba(255, 79, 18, 1)"
    assert expected_color in actual_color, (
        f"Элемент 'Забыл пароль' не перекрасился в нужный оранжевый цвет! "
        f"Ожидалось: '{expected_color}', но получено: '{actual_color}'"
    )

def test_048_empty_login_field_validation(auth_page):
    """FAU-048: Отправка формы с пустым полем «Логин»"""
    auth_page.click_locator(auth_page.TAB_LOGIN)
    assert auth_page.is_tab_active(auth_page.TAB_LOGIN), "Не удалось переключиться на вкладку 'Логин'!"
    auth_page.clear_field(auth_page.INPUT_USERNAME)
    auth_page.enter(auth_page.INPUT_PASSWORD, "AnyPassword123!")
    auth_page.click_locator(auth_page.BUTTON_LOGIN)
    expected_error = "Введите логин, указанный при регистрации"
    actual_error = auth_page.get_element_text(auth_page.FIELD_ERROR_MESSAGE)
    assert expected_error in actual_error, (
        f"Ожидалась ошибка поля '{expected_error}', "
        f"но интерфейс отобразил: '{actual_error}'"
    )
    # Проверка, что мы остались на той же странице авторизации (форма не отправилась на сервер)
    assert auth_page.URL in auth_page.driver.current_url, (
        f"Произошел несанкционированный редирект! "
        f"Текущий URL: {auth_page.driver.current_url}"
    )

def test_063_help(auth_page):
    """FAU-057: Переход по ссылке «Пользовательское соглашение»"""
    auth_page.click_locator(auth_page.AGREEMENT_LINK)
    auth_page.switch_to_new_tab()
    expected_url_part = "/sso-static/agreement/agreement.html"
    actual_url = auth_page.driver.current_url
    assert expected_url_part in actual_url, (
        f"URL-адрес открывшегося соглашения некорректен! "
        f"Ожидалась часть пути: '{expected_url_part}', но текущий URL: '{actual_url}'"
    )