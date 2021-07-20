from datetime import datetime, timedelta


def get_data_range(dias: int, convert=False) -> list:
    presente = datetime.today().date()
    passado = presente - timedelta(days=int(dias))

    if convert:
        return [convert_date_to_datetime(passado), convert_date_to_datetime(presente, inicio=False)]

    return [passado, presente]


def convert_date_to_datetime(date_value, inicio=True):
    if inicio:
        return date_value.strftime("%Y-%m-%d") + " 00:00:00"
    return date_value.strftime("%Y-%m-%d") + " 23:59:59"
