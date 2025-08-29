from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import pandas as pd
import re
import json

def extract_ratings_from_card(card_el):
    """
    card_el - элемент фильма
    возвращает словарь с рейтингами (только myRating, если найден)
    """
    my_rating = None
    text = card_el.text

    # ищем элемент "оценил: 4" или "оценил - 4"
    m_my = re.search(r"оценил\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?)", text, re.IGNORECASE)
    if m_my:
        my_rating = float(m_my.group(1))

    if my_rating is None:
        return {}
    return {
        "myRating": my_rating
    }

def extract_year_from_card(card_el):
    """
      Ищем год из названия фильма:
    - Год: 2019 или Год - 2019 и т.п.
    - год внутри текста
    - Любой год где угодно в тексте
    - Возвращает пустую строку года если не найден.
    """
    text_all = (card_el.text or "")
    # Год: 2019
    m_year = re.search(r"Год\s*[:\-]?\s*([12][0-9]{3})", text_all, re.IGNORECASE)
    if m_year:
        return m_year.group(1)

    # Год внутри заголовка фильма
    m_parenth = re.search(r"$(\s*[12][0-9]{3}\s*)$", text_all)
    if m_parenth:
        extracted_year = m_parenth.group(1).strip()
        return extracted_year

    # Любой год 1900-2099 в тексте названия фильма
    m_any = re.search(r"\b(19|20)[0-9]{2}\b", text_all)
    if m_any:
        return m_any.group(0)
    return ""

chrome_options = Options()
# Выключаем визуальный режим браузера chrome
chrome_options.add_argument("--headless")  # скрываем браузер chrome
# Настройка драйвера браузер chrome
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)

try:
    # Перейдите на страницу профиля пользователя с фильмами и оценками
    profile_url = 'https://www.film.ru/user/1464023/folder/viewed/1'
    driver.get(profile_url)

    # Подождать загрузку страницы пользователя раздела "просмотрено"
    try:
        wait.until(EC.presence_of_element_located((By.ID, 'list_content')))
    except Exception as e:
        print("Раздел 'просмотрено' не найден или загрузка занимает больше времени:", e)

    # Прокрутка до конца страницы, чтобы подгрузились все фильмы (автоматизировано)
    def scroll_to_bottom():
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    scroll_to_bottom()

        # Находим раздел "просмотрено"
    try:
        list_content_div = driver.find_element(By.ID, 'list_content')
        films_elements = list_content_div.find_elements(By.CSS_SELECTOR, 'div.lk_list_movies')
    except Exception as e:
        print("Раздел 'просмотрено' не найден:", e)
        films_elements = []

    films_data = []
    seen_titles = set()

    for el in films_elements:
        # Название фильма
        try:
            title_el = el.find_element(By.TAG_NAME, 'strong')
            title = title_el.text.strip()
        except NoSuchElementException:
            try:
                img_el = el.find_element(By.TAG_NAME, 'img')
                title = img_el.get_attribute('alt').strip()
            except NoSuchElementException:
                title = ''
            except StaleElementReferenceException:
                title = ''
        except StaleElementReferenceException:
            title = ''

        # Год выпуска фильма
        year = extract_year_from_card(el)

        # Рейтинг фильма
        ratings = extract_ratings_from_card(el)
        rating_val = ratings.get("myRating") if ratings else None

        # Пропускаем дубликаты по названию
        if not title or title in seen_titles:
            continue

        film_entry = {
            'Название фильма': title,
            'Год': year,
            'Оценка': rating_val
        }
        # Добавляем дополнительные поля
        films_data.append(film_entry)

    # Выводим собранные данные
    print(f"Найдено фильмов: {len(films_data)}")
    for film in films_data:
        print(
            f"Название: {film.get('Название фильма','')}, "
            f"Год: {film.get('Год','')}, "
            f"Оценка: {film.get('Оценка','')}, "
            )

finally:
    driver.quit()

# Сохранение в файл Excel "films.xlsx"
df = pd.DataFrame(films_data)
df.to_excel("films.xlsx", index=False)

# Сохранение в файл JSON "films.json"
with open("films.json", "w", encoding="utf-8") as f_json:
    json.dump({"films": films_data}, f_json, ensure_ascii=False, indent=2)


