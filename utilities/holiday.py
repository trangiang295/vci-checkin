from datetime import datetime, timedelta
from lunarcalendar import Converter, Solar

solar_holiday = [
    (1, 1),
    (30, 4),
    (1, 5),
    (2, 9)
]

lunar_holiday = [
    (10, 3),
    (29, 12),
    (30, 12),
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1)
]


def is_holiday():
    now = datetime.utcnow() + timedelta(hours=7)
    for x in solar_holiday:
        if x[0] == now.day and x[1] == now.month:
            return True
    solar = Solar(now.year, now.month, now.day)
    lunar = Converter.Solar2Lunar(solar)
    for x in lunar_holiday:
        if x[0] == lunar.day and x[1] == lunar.month:
            return True
    return False
