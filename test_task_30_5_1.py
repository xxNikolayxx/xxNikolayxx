import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from collections import Counter

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.find_element(By.ID, 'email').send_keys('ttnikott@mail.ru')
    driver.find_element(By.ID, 'pass').send_keys('12345')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.get('https://petfriends.skillfactory.ru/my_pets')
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
    yield driver
    driver.quit()

def test_collect_pets_data(driver):
    # Находим все карточки питомцев
    cards = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr')
    assert len(cards) > 0, "На странице нет питомцев"

    names = []
    breeds = []
    ages = []
    pets_with_photos = 0

    # Собираем данные по каждому питомцу
    for card in cards:
        cells = card.find_elements(By.CSS_SELECTOR, 'td')
        name = cells[0].text.strip()
        breed = cells[1].text.strip()
        age_str = cells[2].text.strip()

        # Для повторяющихся питомцев используем комбинацию имени, породы и возраста
        age_match = re.search(r'(\d+)', age_str)
        age = int(age_match.group()) if age_match else None

        # Проверка и сбор данных
        if name:
            names.append(name)
        if breed:
            breeds.append(breed)
        if age is not None:
            ages.append(age)

        # Проверка фото питомца
        images = card.find_elements(By.CSS_SELECTOR, 'img')
        if images:
            img_src = images[0].get_attribute('src')
            if img_src and (img_src.startswith('http') or 'data:image' in img_src):
                pets_with_photos += 1

    # Формируем список кортежей для определения повторяющихся питомцев
    pet_tuples = []
    for card in cards:
        cells = card.find_elements(By.CSS_SELECTOR, 'td')
        name = cells[0].text.strip()
        breed = cells[1].text.strip()
        age_str = cells[2].text.strip()
        age_match = re.search(r'(\d+)', age_str)
        age = int(age_match.group()) if age_match else None
        pet_tuples.append((name, breed, age))

    # Подсчет повторяющихся питомцев (кортежей, встречающихся более одного раза)
    pet_counter = Counter(pet_tuples)
    repeated_pets = {k: v for k, v in pet_counter.items() if v > 1}
    #repeated_count = sum(repeated_pets.values())  # Общее число повторяющихся питомцев
    print()
    print(f"Общее число питомцев: {len(names)}")
    print(f"Количество питомцев с фото: {pets_with_photos}")
    print(f"Общее количество повторяющихся питомцев (имя, порода, возраст): {len(repeated_pets)}")
    if repeated_pets:
        print("Повторяющиеся питомцы и их количество:")
        for pet, count in repeated_pets.items():
            print(f"{pet}: {count} раза")

    # Получаем уникальные имена
    unique_names = set(names)
    print("Неповторяющиеся имена питомцев:", len(unique_names))
