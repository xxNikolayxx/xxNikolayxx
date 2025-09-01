from Task_24_7_2.api import PetFriends
from Task_24_7_2.settings import valid_email, valid_password
import os

pf = PetFriends()

def test_add_new_pet_without_photo_valid_data(name='Барбоскин', animal_type='двортерьер', age='4'):
    """Проверяем, что можно добавить питомца с корректными данными без фото """

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фото
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
#------------------------------------------------------------------------------------------------------------
def test_add_photo_pet(pet_photo='images/cat1.jpg'):
    """Проверяем возможность добавление фото питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200,201 и фото питомца соответствует заданному
        assert status in (200, 201)
        assert isinstance(result, dict)
        assert 'pet_photo' in result
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#---------------------------------------------------------------------------------------------------------
def test_add_new_pet_with_long_name(name='Барбоскин'*100, animal_type='двортерьер', age='4', pet_photo='images/cat1.jpg'):
    """Проверяем, что можно добавить питомца с некорректными данными, например (с длинным именем)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

#-------------------------------------------------------------------------------------------------------
def test_add_new_pet_with_long_type(name='Барбоскин', animal_type='двортерьер'*100, age='4', pet_photo='images/cat1.jpg'):
    """Проверяем, что можно добавить питомца с некорректными данными, например (с длинным типом животного)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
#----------------------------------------------------------------------------------------------------------
def test_get_all_pets_without_valid_password(filter=''):
    """ Проверяем, если невалидный пароль, то тест не пройден."""

    _, auth_key = pf.get_api_key(valid_email, '123456')
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

#-----------------------------------------------------------------------------------------------------------
def test_get_all_pets_without_valid_email(filter=''):
    """ Проверяем, если невалидный email, то тест не пройден."""

    _, auth_key = pf.get_api_key('ttnikott@gdfmail.com', valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0
#------------------------------------------------------------------------------------------------------------
def test_successful_delete_self_pet_number():
    """Проверяем возможность удаления не первого в списке питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id не первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][2]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

#--------------------------------------------------------------------------------------------------------------------
def test_add_photo_pet_not_jpeg(pet_photo='images/screen_42.png'):
    """Проверяем возможность добавление фото питомца с расширением png"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200,201 и фото питомца соответствует заданному
        assert status in (200, 201)
        assert isinstance(result, dict)
        assert 'pet_photo' in result
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
#----------------------------------------------------------------------------------------------
def test_add_new_pet_with_long_age_down(name='Барбоскин', animal_type='двортерьер', age='-48000', pet_photo='images/p1040103.jpg'):
    """Проверяем, что можно добавить питомца с некорректными данными, например (с отрицательным и много числительным возрастом)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

#---------------------------------------------------------------------------------------------------------------
def test_add_new_pet_with_special_symbols_name(name='!"№% :?*()[]{}/=+-\|', animal_type='двортерьер', age='5', pet_photo='images/p1040103.jpg'):
    """Проверяем, что можно добавить питомца с некорректными данными, например (со специальными символами)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name