def test_004_double_name_with_dash(reg_page):
    """REG-004: Ввод двойного имени со знаком тире (-)"""
    reg_page.enter(reg_page.INPUT_FIRSTNAME, "Анна-Мария", submit=True)
    assert not reg_page.is_element_visible(reg_page.FIRSTNAME_ERROR), (
        f"Появилась непредвиденная ошибка валидации под полем 'Имя': "
        f"'{reg_page.get_element_text(reg_page.FIRSTNAME_ERROR)}'"
    )

def test_reg_005_minimal_length_with_dash_bug(reg_page):
    """REG-005: Имя, состоящее только из буквы кириллицы и знака тире (минимальная длина с тире)"""
    invalid_by_fact_name = "А-"
    reg_page.enter(reg_page.INPUT_FIRSTNAME, invalid_by_fact_name, submit=True)
    assert not reg_page.is_element_visible(reg_page.FIRSTNAME_ERROR), (
        f"Система заблокировала валидное по ТЗ имя: {invalid_by_fact_name}"
        f" и выдала ошибку: '{reg_page.get_element_text(reg_page.FIRSTNAME_ERROR)}'"
    )

def test_reg_023_lastname_latin_validation(reg_page):
    """REG-023: Фамилия, ввод букв латинского алфавита (латиница)"""
    latin_lastname = "Lastname"
    reg_page.enter(reg_page.INPUT_LASTNAME, latin_lastname, submit=True)
    assert reg_page.is_element_visible(reg_page.LASTNAME_ERROR), (
        f"Ошибка валидации под полем 'Фамилия' не появилась после ввода латиницы '{latin_lastname}'!"
    )
    expected_error_text = "Необходимо заполнить поле кириллицей"
    actual_error_text = reg_page.get_element_text(reg_page.LASTNAME_ERROR)
    assert expected_error_text in actual_error_text, (
        f"Текст ошибки некорректен! Ожидалось упоминание кириллицы, "
        f"но на экране отображается: '{actual_error_text}'"
    )

def test_reg_031_lastname_max_length_validation(reg_page):
    """REG-031: Фамилия, граничное значение — ввод 31 символа (превышение лимита в 30 знаков)"""
    long_lastname = "Абвгдеёжзийклмнопрстуфхцчшщъыьэюя"[:31]  # Обрезаем или берем готовую строку нужной длины
    reg_page.enter(reg_page.INPUT_LASTNAME, long_lastname, submit=True)
    assert reg_page.is_element_visible(reg_page.LASTNAME_ERROR), (
        f"Ошибка валидации длины не появилась под полем 'Фамилия' после ввода 31 символа!"
    )
    expected_error_part = "От 2 до 30 символов"
    actual_error = reg_page.get_element_text(reg_page.LASTNAME_ERROR)
    assert expected_error_part in actual_error, (
        f"Текст ошибки некорректен! Ожидалось упоминание лимита в 30 символов, "
        f"но фактически на экране отображается: '{actual_error}'"
    )

def test_reg_032_default_region_value_bug(reg_page):
    """REG-032: Проверка значения региона по умолчанию (Ожидается падение из-за бага)"""
    actual_region = reg_page.get_default_region_value()
    expected_region = "Москва"
    assert actual_region == expected_region, (
        f"По умолчанию должен быть город '{expected_region}', "
        f"но фактически в поле отображается: '{actual_region}'"
    )

def test_reg_044_belarus_phone_validation(reg_page):
    """REG-044: Ввод номера телефона в формате Беларуси (+375)"""
    belarus_phone = "+375291112233"
    reg_page.enter(reg_page.INPUT_ADDRESS, belarus_phone, submit=True)
    assert not reg_page.is_element_visible(reg_page.ADDRESS_ERROR), (
        f"Система отклонила корректный номер Беларуси: {belarus_phone}. "
        f"Фактический текст ошибки на экране: '{reg_page.get_element_text(reg_page.ADDRESS_ERROR)}'"
    )

def test_reg_051_invalid_email_without_at_symbol(reg_page):
    """REG-058: Ввод строки без символа «@» (Проверка базового признака email-адреса)"""
    invalid_email = "example.email.ru"
    reg_page.enter(reg_page.INPUT_ADDRESS, invalid_email, submit=True)
    assert reg_page.is_element_visible(reg_page.ADDRESS_ERROR), (
        f"Ошибка валидации не появилась под полем контакта после ввода строки без '@': '{invalid_email}'!"
    )
    expected_error_part = "или email в формате example@email.ru"
    actual_error = reg_page.get_element_text(reg_page.ADDRESS_ERROR)
    assert expected_error_part in actual_error, (
        f"Текст ошибки некорректен! Ожидалось упоминание правильного формата email, "
        f"но фактически на экране: '{actual_error}'"
    )

def test_reg_058_short_password_validation(reg_page):
    """REG-058: Пароль менее 8 символов"""
    short_password = "Pass123"
    reg_page.enter(reg_page.INPUT_PASSWORD, short_password, submit=True)
    assert reg_page.is_element_visible(reg_page.PASSWORD_ERROR), (
        f"Ошибка валидации не появилась под полем 'Пароль' после ввода короткого значения '{short_password}'!"
    )
    expected_error = "Длина пароля должна быть не менее 8 символов"
    actual_error = reg_page.get_element_text(reg_page.PASSWORD_ERROR)
    assert expected_error in actual_error, (
        f"Текст ошибки некорректен! Ожидалось: '{expected_error}', "
        f"но фактически на экране: '{actual_error}'"
    )

def test_reg_062_passwords_do_not_match_validation(reg_page):
    """REG-062: Пароли не совпадают"""
    valid_password = "Pass1234"
    reg_page.enter(reg_page.INPUT_PASSWORD, valid_password)
    mismatched_password = "pass1234"
    reg_page.enter(reg_page.INPUT_PASSWORD_CONFIRM, mismatched_password, submit=True)
    assert reg_page.is_element_visible(reg_page.PASSWORD_CONFIRM_ERROR), (
        "Ошибка 'Пароли не совпадают' не появилась под полем подтверждения пароля!"
    )
    expected_error = "Пароли не совпадают"
    actual_error = reg_page.get_element_text(reg_page.PASSWORD_CONFIRM_ERROR)
    assert expected_error in actual_error, (
        f"Текст ошибки несовпадения некорректен! Ожидалось: '{expected_error}', "
        f"но фактически отображается: '{actual_error}'"
    )




