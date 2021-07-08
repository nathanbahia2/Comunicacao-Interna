from datetime import datetime, timedelta


def get_data_range(dias: int) -> list:
    presente = datetime.today().date()
    passado = presente - timedelta(days=int(dias))
    return [passado, presente]
