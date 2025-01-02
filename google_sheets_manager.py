import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date, timedelta

from schedule_generator import generate_schedule_data, month_map  # Импортируем функцию

def authenticate_google_sheets(json_keyfile: str, scope: list) -> gspread.Client:
    """
    Функция для аутентификации в Google Sheets API.

    :param json_keyfile: Путь к файлу с учетными данными.
    :param scope: Список областей доступа.
    :return: Авторизованный клиент gspread.
    """
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(creds)
    return client


def initialize_schedule(sheet: gspread.Worksheet, month_name: str) -> None:
    """
    Инициализирует таблицу заголовками.

    :param sheet: Лист таблицы, который нужно обновить.
    :param month_name: Название месяца для заголовка.
    """
    sheet.update("A1", [[month_name, 'Филипп', "Александр", "Роман"]])


def update_schedule(sheet: gspread.Spreadsheet, data: list) -> None:
    """
    Обновляет таблицу данными графика.

    :param sheet: Лист таблицы, который нужно обновить.
    :param data: Данные для записи в таблицу.
    """
    sheet.update("A2", data)


def get_date() -> tuple:
    """
    Возвращает начальную и конечную дату для формирования графика.

    :return: Кортеж с датами (start_date, end_date).
    """
    # Определяем start_date и end_date заранее
    end_date = datetime(2024, 3, 31)
    start_date = datetime(2024, 3, 1)

    return start_date, end_date


def main():
    # Устанавливаем область доступа для API
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']

    # Путь к файлу с учетными данными
    json_keyfile = 'handy-hexagon-441310-n5-3a7c43d6b046.json'

    # Авторизация и создание клиента для работы с Google Sheets
    client = authenticate_google_sheets(json_keyfile, scope)

    # Открытие таблицы по URL
    spreadsheet = client.open_by_url(
        'https://docs.google.com/spreadsheets/d/1W2P0Bm5N1IF1MvIcIqNgKhtqaAlIdKJY6u8whDkv9s8/edit?usp=sharing')

    # Получаем начальную и конечную дату
    start_date, end_date = get_date()

    # Генерация данных и имени месяца
    data, month_name = generate_schedule_data(start_date, end_date)

    try:
        # Открываем таблицу
        sheet = spreadsheet.get_worksheet(int(end_date.month))  # Пытаемся получить указанный лист

    except gspread.exceptions.WorksheetNotFound:
        month_name = month_map[int(end_date.month)]  # Получаем название месяца
        month_end_date = int(end_date.day) # Получаем дату конца месяца
        sheet = spreadsheet.add_worksheet(title=month_name, rows=month_end_date, cols="4")

    # Инициализация заголовков
    initialize_schedule(sheet, month_name)

    # Обновление таблицы
    update_schedule(sheet, data)

    print("График успешно заполнен!")


if __name__ == "__main__":
    main()
