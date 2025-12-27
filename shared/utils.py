from .config import settings
from datetime import datetime
from zoneinfo import ZoneInfo

def get_hora_peru():
    return datetime.now(ZoneInfo(settings.TIMEZONE))

