# schedule_generator.py
from datetime import datetime, timedelta

month_map = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь"
}

def generate_schedule(start_date: datetime, end_date: datetime) -> list:
    """
    Генерирует график для Филиппа, Александра и Романа.

    :param start_date: Дата начала периода.
    :param end_date: Дата окончания периода.
    :return: Список с данными для записи в таблицу.
    """
    phil_counter = 0  # Счетчик дней для Филиппа
    alex_counter = 2  # Счетчик дней для Александра
    roman_counter = -2  # Роман подключается на 3-й день

    data = []  # Список для хранения данных

    while start_date <= end_date:
        phil_status = ""
        alex_status = ""
        roman_status = ""

        # Логика для каждого работника (4 дня работы, 2 выходных)
        phil_status = "Работает" if phil_counter % 6 < 4 else ""
        alex_status = "Работает" if alex_counter % 6 < 4 else ""
        roman_status = "Работает" if roman_counter % 6 < 4 else ""

        # Добавляем строку в данные
        data.append([start_date.strftime("%d.%m"), phil_status, alex_status, roman_status])

        # Обновляем счетчики
        phil_counter += 1
        alex_counter += 1
        roman_counter += 1

        # Переход на следующий день
        start_date += timedelta(days=1)

    return data

def get_month_name(date: datetime) -> str:
    """
    Возвращает название месяца для заданной даты.

    :param date: Дата для извлечения месяца.
    :return: Название месяца.
    """
    return month_map[int(date.month)]

def generate_schedule_data(start_date: datetime, end_date: datetime) -> tuple:
    """
    Генерирует данные для графика и название месяца для листа.

    :param start_date: Дата начала.
    :param end_date: Дата окончания.
    :return: Кортеж (данные для графика, название месяца).
    """
    data = generate_schedule(start_date, end_date)
    month_name = get_month_name(end_date)
    return data, month_name
