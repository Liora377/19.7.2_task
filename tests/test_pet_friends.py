from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result  # в результате возвращается ключ


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Tom', animal_type='простокот',
                                     age='2', pet_photo='images/c1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/c1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Томыч', animal_type='Котэ', age=3):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Тест 1

def test_add_new_pet_with_valid_data_without_photo(name='Tom', animal_type='простокот',
                                     age='2'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

# Тест 2

def test_add_photo_of_pet_with_valid_data(pet_photo='images/c1.jpg'):
    """Проверяем что можно добавить фото к имеющемуся питомцу с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key и список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200 и фото присутствует
        assert status == 200
        assert result['pet_photo'] != ''
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Тест 3

def test_get_api_key_with_unvalid_password(email=valid_email, password='7895'):
    """ Проверяем, что запрос api ключа с невалидным password возвращает статус 403.
    Код ошибки означает, что указанная комбинация электронной почты пользователя и пароля неверна."""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    # assert 'key' in result  # в результате возвращается ключ

# Тест 4

def test_get_api_key_with_unvalid_email(email='cheese@mail.ru', password=valid_password):
    """ Проверяем, что запрос api ключа с невалидным email возвращает статус 403.
    Код ошибки означает, что указанная комбинация электронной почты пользователя и пароля неверна."""
    status, result = pf.get_api_key(email, password)
    assert status == 403

#Тест 5

def test_get_api_key_with_valid_email_and_without_password(email=valid_email, password=''):
    """ Проверяем, что запрос api ключа с валидными mail и без password возвращает статус 403.
    Код ошибки означает, что указанная комбинация электронной почты пользователя и пароля неверна."""
    status, result = pf.get_api_key(email, password)
    assert status == 403

# Тест 6

def test_get_all_pets_with_unvalid_key(filter=''):
    """ Проверяем, что запрос всех питомцев с неверным api ключом выдает код 403.
    Код ошибки означает, что предоставленный auth_key неверен."""
    auth_key = {"key": "ea738148a1f19838e1c5d1413877f3691a3731380e733e87"}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

# Тест 7

def test_unsuccessful_update_self_pet_info_with_str_age(name='Кекс', animal_type='Котэ', age='проверка'):
    """Проверяем, что при обновлении информации о питомце со строкой в поле возраста тест
    выдает код 400 - неверные данные."""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 400 и имя питомца соответствует заданному
        assert status == 400
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Тест 8

def test_add_new_pet_without_name(name='', animal_type='простокот',
                                     age='2', pet_photo='images/c1.jpg'):
    """Проверяем, что при добавлении питомца без имени выдает ошибку 400.
    Код ошибки означает, что предоставленные данные неверны"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

# Тест 9

def test_add_new_pet_with_unvalid_key(name='Tom', animal_type='простокот',
                                     age='2', pet_photo='images/c1.jpg'):
    """Проверяем, что при добавлении питомца с невалидным ключом выдает ошибку 403.
    Код ошибки означает, что предоставленный auth_key неверен"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    auth_key = {"key": "ea738148a1f19838e1c5d1413877f3691a3731380e733e87"}
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


# Тест 10

def test_unsuccessful_delete_someone_elses_pet():
    """Проверяем, что при удалении чужого питомца из базы выдает ошибку. Не возможен код 200"""

    # Получаем ключ auth_key и запрашиваем список всех питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    # Проверяем - если список питомцев пустой, то добавляем нового и опять запрашиваем список всеех питомцев
    if len(all_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/c1.jpg")
        _, all_pets = pf.get_list_of_pets(auth_key, "")

    # Берём id любого питомца из списка и отправляем запрос на удаление
    pet_id = all_pets['pets'][2]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список всех питомцев
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    assert status != 200


