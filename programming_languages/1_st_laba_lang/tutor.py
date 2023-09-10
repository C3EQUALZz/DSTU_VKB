import calendar
from datetime import datetime

if (month := int(input())) <= 12:
    res = calendar.month(datetime.now().year, month)
    count_days = calendar.monthrange(datetime.now().year, month)[1]
    name = calendar.month_name[month]
    print(f"Название месяца - {name}, количество дней - {count_days}", res, sep='\n')
else:
    raise ValueError("Неправильная дата")
