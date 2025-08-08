# 1. Какой номер самого дорого заказа за июль?
import json
# считать данные из файла и преобразовать их в словарь
with open("orders_july_2023.json", "r") as my_file:
    dataJson = json.load(my_file)
# Вывод словаря в консоль
print(dataJson)

max_price = 0
max_order = ''
# цикл по заказам
for order_num, orders_data in dataJson.items():
    # получаем стоимость заказа
    price = orders_data['price']
    # если стоимость больше максимальной - запоминаем номер и стоимость заказа
    if price > max_price:
        max_order = order_num
        max_price = price
print(f'Номер заказа: {max_order}, с самой большой стоимостью заказа: {max_price}')
#------------------------------------------------------------------------------------------------------------
# 2. Какой номер заказа с самым большим количеством товаров?
max_tovar = 0
max_order = ''
# цикл по заказам
for order_num, orders_data in dataJson.items():
    # получаем количество товаров
    tovar = orders_data['quantity']
    # если количество товаров больше максимальной - запоминаем номер и количество товаров
    if tovar > max_tovar:
        max_order = order_num
        max_tovar = tovar
print(f'Номер заказа: {max_order}, с самым большим количеством товаров: {max_tovar}')
#-------------------------------------------------------------------------------------------------------------
# 3. В какой день в июле было сделано больше всего заказов?
from collections import defaultdict

day_counts = defaultdict(int)

for order_num, order_data in dataJson.items():
    date_str = order_data.get('date', '')
    if date_str.startswith('2023-07'):
        # Предполагается формат даты 'YYYY-MM-DD'
        day = date_str[8:10]
        day_counts[day] += 1

if day_counts:
    max_day = max(day_counts, key=day_counts.get)
    max_count = day_counts[max_day]
    print(f"День с наибольшим количеством заказов: 2023-07-{max_day} — {max_count} заказов")
else:
    print("Нет заказов за июль.")
#---------------------------------------------------------------------------------------------------------
# 4. Какой пользователь сделал самое большое количество заказов за июль?
user_order_counts = {}

for order_num, order_data in dataJson.items():
    date_str = order_data.get('date', '')
    if date_str.startswith('2023-07'):
        user_id = order_data.get('user_id')
        if user_id is not None:
            user_order_counts[user_id] = user_order_counts.get(user_id, 0) + 1

if user_order_counts:
    max_user = max(user_order_counts, key=user_order_counts.get)
    max_orders = user_order_counts[max_user]
    print(f"Пользователь с ID {max_user} сделал наибольшее количество заказов за июль: {max_orders}")
else:
    print("Нет заказов за июль.")

#-----------------------------------------------------------------------------------------------------------
# 5. У какого пользователя самая большая суммарная стоимость заказов за июль?
user_totals = {}

for order_num, order_data in dataJson.items():
    date_str = order_data.get('date', '')
    if date_str.startswith('2023-07'):
        user_id = order_data.get('user_id')
        price = order_data.get('price', 0)
        try:
            price = float(price)
        except (TypeError, ValueError):
            price = 0
        if user_id is not None:
            user_totals[user_id] = user_totals.get(user_id, 0) + price

if user_totals:
    max_user = max(user_totals, key=user_totals.get)
    max_value = user_totals[max_user]
    print(f"Пользователь с ID {max_user} имеет самую большую сумму заказов за июль: {max_value:.2f}")
else:
    print("Нет заказов за июль.")
#-----------------------------------------------------------------------------------------------------
# 6. Какая средняя стоимость заказа была в июле?
total_order_value = 0
count_orders = 0

for order_num, order_data in dataJson.items():
    date_str = order_data.get('date', '')
    if date_str.startswith('2023-07'):
        price = order_data.get('price', 0)
        try:
            price = float(price)
        except (TypeError, ValueError):
            price = 0
        total_order_value += price
        count_orders += 1

if count_orders > 0:
    average_order_price = total_order_value / count_orders
    print(f"Средняя стоимость заказа в июле: {average_order_price:.2f}")
else:
    print("Нет заказов за июль.")

#------------------------------------------------------------------------------------------------------
# 7. Какая средняя стоимость товаров в июле?
total_value_of_goods = 0
total_quantity = 0

for order_num, order_data in dataJson.items():
    date_str = order_data.get('date', '')
    if date_str.startswith('2023-07'):
        quantity = order_data.get('quantity', 0)
        price = order_data.get('price', 0)
        try:
            quantity = int(quantity)
            price = float(price)
        except (TypeError, ValueError):
            quantity = 0
            price = 0
        # Средняя цена за товар в этом заказе
        if quantity > 0:
            total_value_of_goods += price
            total_quantity += quantity

if total_quantity > 0:
    average_price_per_item = total_value_of_goods / total_quantity
    print(f"Средняя стоимость товара в июле: {average_price_per_item:.2f}")
else:
    print("Нет данных о товарах за июль.")
