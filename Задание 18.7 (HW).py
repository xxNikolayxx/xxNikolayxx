import random

# список учеников
students = ['Аполлон', 'Ярослав', 'Александра', 'Дарья', 'Ангелина']
# отсортируем список учеников
students.sort()
# список предметов
classes = ['Математика', 'Русский язык', 'Информатика']
# пустой словарь с оценками по каждому ученику и предмету
students_marks = {}
# сгенерируем данные по оценкам:
# цикл по ученикам
for student in students:  # 1 итерация: student = 'Александра'
    students_marks[student] = {}  # 1 итерация: students_marks['Александра'] = {}
    # цикл по предметам
    for class_ in classes:  # 1 итерация: class_ = 'Математика'
        marks = [random.randint(1, 5) for i in range(3)]  # генерируем список из 3х случайных оценок
        students_marks[student][class_] = marks  # students_marks['Александра']['Математика'] = [5, 5, 5]
# выводим получившийся словарь с оценками:
for student in students:
    print(f'''{student}
            {students_marks[student]}''')

print('''
        Список команд:
        1. Добавить оценки ученика по предмету
        2. Вывод информации по ученикам, предметам, оценкам.
        3. Редактирование учеников, предметов, оценок.
        4. Удаление учеников, предметов, оценок.
        5. Выход из программы
        ''')

while True:
    user_input= input('Введите команду главного меню (для выхода введите 5): - > ')
    if user_input.isdigit():
        number = int(user_input)
        command = number
        if command == 1 and user_input.isdigit():
            print('1. Добавить оценку ученика по предмету')
        # считываем имя ученика
            student = input('Введите имя ученика: ')
        # считываем название предмета
            class_ = input('Введите предмет: ')
        # считываем оценку
            mark = int(input('Введите оценку: '))
        # если данные введены верно
            if student in students_marks.keys() and class_ in students_marks[student].keys():
            # добавляем новую оценку для ученика по предмету
                students_marks[student][class_].append(mark)
                print(f'Для {student} по предмету {class_} добавлена оценка {mark}')
        # неверно введены название предмета или имя ученика
            else:
                print('ОШИБКА: неверное имя ученика или название предмета')

        elif command == 2:
            print('2. Вывод информации по ученикам, предметам, оценкам. ')
            print('''
                    Список команд под меню:
                    1. Вывести средний балл по всем предметам всех учеников
                    2. Вывести все оценки по всем ученикам
                    3. Вывести средний балл по всем предметам по ученику
                    4. Вывести все оценки по ученику
                    5. Вывести средний бал по каждому предмету для одного ученика
                    6. Выход из под меню
                    ''')
            while True:
                user_input = input('Введите команду под меню (для выхода нажмите 6): - > ')
                if user_input.isdigit():
                    number = int(user_input)
                    command = number
                    if command == 1 and user_input.isdigit():
                        print('1. Вывести средний балл по всем предметам по каждому ученику')
                         # цикл по ученикам
                        for student, subjects in students_marks.items():
                            total_grades = []
                            for grades in subjects.values():
                                total_grades.extend(grades)
                            if total_grades:
                                average = sum(total_grades) / len(total_grades)
                                print(f'Средний балл по всем предметам у {student} — {average:.2f}')
                            else:
                                print(f'У {student} нет оценок.')
                    elif command == 2:
                        print('2. Вывести все оценки по всем ученикам')
                        # выводим словарь с оценками:
                        # цикл по ученикам
                        for student, classes in students_marks.items():
                            print(student)
                            # цикл по предметам
                            for class_, mark in classes.items():
                                print(f'\t{class_} - {mark}')
                            print()
                    elif command == 3:
                        print('3. Вывести средний балл по всем предметам по ученику')
                        # считываем имя ученика
                        student = input('Введите имя ученика: ')
                        if student in students_marks:
                            all_grades = []
                            # цикл по предметам
                            for grades in students_marks[student].values():
                                # находим сумму оценок по предмету
                                all_grades.extend(grades)
                            if all_grades:
                                average = sum(all_grades) / len(all_grades)
                                print(f'{student} - {average:.2f}')
                            print()
                        else:
                            print('ОШИБКА: неверное имя ученика')

                    elif command == 4:
                        print('4. Вывести все оценки по ученику')
                        # считываем имя ученика
                        student = input('Введите имя ученика: ')
                        if student in students_marks:
                            # выводим словарь с оценками одного ученика:
                            print(student)
                            for class_, mark in students_marks[student].items():
                                print(f'\t{class_}: - {mark}')
                            print()
                        else:
                            print('ОШИБКА: неверное имя ученика')

                    elif command == 5:
                        print('5. Вывести средний бал по каждому предмету для одного ученика')
                        student = input('Введите имя ученика: ')
                        if student in students_marks:
                            subjects = students_marks[student]
                            for subject, grades in subjects.items():
                                if grades:
                                    average = sum(grades) / len(grades)
                                    print(f'Средний бал по предмету "{subject}" — {average:.2f}')
                                else:
                                    print(f'У {student} по предмету "{subject}" нет оценок.')
                        else:
                            print('Такого ученика нет.')

                    elif command == 6:
                        print('6. Выход из под меню вывода')
                        break
                else:
                    print('ОШИБКА: неверный пункт под меню')

        elif command == 3:
            print('3. Редактирование учеников, предметов, оценок. ')
            print('''
                                Список команд меню редактора:
                                1. Редактировать оценки ученика по предмету
                                2. Редактировать имя ученика
                                3. Редактировать предмет ученика
                                4. Выход из меню редактора
                                ''')
            while True:
                user_input = input('Введите команду меню редактора (для выхода введите 4): - > ')
                if user_input.isdigit():
                    number = int(user_input)
                    command = number
                    if command == 1 and user_input.isdigit():
                        print('1. Редактировать оценку ученика по предмету')
                        # считываем имя ученика
                        student = input('Введите имя ученика: ')
                        # считываем название предмета
                        class_ = input('Введите предмет: ')
                        # считываем оценку
                        mark = int(input('Введите оценку: '))
                        # считываем новую оценку
                        new_mark = int(input('Введите новую оценку: '))
                        # если данные введены верно
                        if student in students_marks.keys() and class_ in students_marks[student].keys():
                            # редактируем оценку для ученика по предмету
                            print('Редактируемая оценка: ', mark)
                            print(students_marks)
                            marks_list = students_marks[student][class_]
                            if mark in marks_list:
                                # заменяем первую найденную оценку
                                index = marks_list.index(mark)
                                marks_list[index] = new_mark
                                print(f'Оценка {mark} у {student} по предмету {class_} заменена на {new_mark}.')
                                print('Запись отредактирована')
                            else:
                                print(f'Оценка {mark} не найдена у {student} по предмету {class_}.')
                                print('Запись не отредактирована')
                        # неверно введены название предмета или имя ученика
                        else:
                            print('ОШИБКА: неверное имя ученика или название предмета')
                    elif command == 2:
                        print('2. Редактировать имя ученика ')
                        # считываем имя ученика
                        student = input('Введите имя ученика: ')
                        # считываем новое имя ученика
                        new_student = input('Введите новое имя ученика: ')
                        # если данные введены верно
                        if student in students_marks:
                            # редактируем имя ученика
                            print('Редактируемое имя: ', student)
                            students_marks[new_student] = students_marks.pop(student)
                            print(f'имя {student} заменена на {new_student}.')
                            print('Запись отредактирована')
                        else:
                            # неверно введены название предмета или имя ученика
                            print(f'имя не найдено ')
                            print('Запись не отредактирована')
                    elif command == 3:
                        print('3. Редактировать предмет ученика ')
                        student = input('Введите имя ученика: ')
                        class_ = input('Введите название предмета для редактирования: ')
                        new_class_ = input('Введите новое название предмета: ')
                        if student in students_marks:
                            if class_ in students_marks[student]:
                                marks = students_marks[student].pop(class_)
                                students_marks[student][new_class_] = marks
                                print(f'предмет {class_} заменена на {new_class_}.')
                            else:
                                print(f'{student} не найден предмет "{class_}".')
                        else:
                            print('Такого ученика нет.')

                    elif command == 4:
                        print('4. Выход из меню редактора')
                        break
                else:
                    print('ОШИБКА: неверный пункт под меню')

        elif command == 4:
            print('4. Удаление учеников, предметов, оценок.')
            print('''
                    Список команд меню редактора:
                    1. Удалить предмет у всех учеников
                    2. Удалить ученика
                    3. Удалить оценки ученика по предмету
                    4. Удалить предмет у одного ученика
                    5. Выход из меню удаления
                    ''')
            while True:
                user_input = input('Введите команду меню удаления (для выхода введите 5): - > ')
                if user_input.isdigit():
                    number = int(user_input)
                    command = number
                    if command == 1 and user_input.isdigit():
                        print('1. Удалить предмет у всех учеников')
                        # считываем название предмета
                        class_ = input('Введите предмет: ')
                        # если данные введены верно
                        print('Удаляемый предмет', class_)
                        # удаляем предмет
                        for student in students_marks:
                            if class_ in students_marks[student]:
                                del students_marks[student][class_]
                                print(f'предмет {class_} удален у', {student})
                            else:
                                # неверно введены название предмета у ученика
                                print(f'не найден предмет {class_} у', {student})

                    elif command == 2:
                        print('2. Удалить ученика')
                        # считываем имя ученика
                        student = input('Введите имя ученика: ')
                        # если данные введены верно
                        if student in students_marks.keys():
                            print('Удаляемый ученик', student)
                            # удаляем ученика
                            del students_marks[student]
                            print(f'Ученик {student} удален')
                        # неверно введены название предмета или имя ученика
                        else:
                            print('ОШИБКА: неверное имя ученика')
                    elif command == 3:
                        print('3. Удалить оценку ученика по предмету')
                        # считываем имя ученика
                        student = input('Введите имя ученика: ')
                        # считываем название предмета
                        class_ = input('Введите предмет: ')
                        # считываем оценку
                        mark = int(input('Введите оценку: '))
                        # если данные введены верно
                        if student in students_marks.keys() and class_ in students_marks[student].keys():
                            # удаляем оценку для ученика по предмету
                            print('Удаляемая оценка', mark)
                            marks_list = students_marks[student][class_]
                            if mark in marks_list:
                                marks_list.remove(mark)
                                print(f'Для {student} по предмету {class_} удалена оценка {mark}')
                            else:
                                print(f'Оценка {mark} не найдена у {student} по предмету {class_}.')
                        # неверно введены название предмета или имя ученика
                        else:
                            print('ОШИБКА: неверное имя ученика или название предмета')
                    elif command == 4:
                        print('4. Удалить предмет у одного ученика')
                        student = input('Введите имя ученика: ')
                        class_ = input('Введите название предмета для удаления: ')
                        if student in students_marks:
                            if class_ in students_marks[student]:
                                del students_marks[student][class_]
                                print(f'Предмет "{class_}" удалён у {student}.')
                            else:
                                print(f'{student} не найден предмет "{class_}".')
                        else:
                            print('Такого ученика нет.')
                    elif command == 5:
                        print('5. Выход из под меню удаления')
                        break
                else:
                    print('ОШИБКА: неверный пункт под меню')
        elif command == 5:
            print('5. Выход из программы')
            break
    else:
        print('ОШИБКА: неверный пункт меню')