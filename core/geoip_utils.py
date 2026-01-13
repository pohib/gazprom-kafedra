import geoip2.database
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_location_from_ip(ip):
    try:
        db_path = getattr(settings, 'GEOIP_PATH', None)
        if not db_path or not os.path.exists(db_path):
            logger.warning(f"🌍 GeoIP файл не найден: {db_path}")
            return 'Не определено', 'Не определено'
        
        logger.debug(f"🌍 GeoIP запрос для IP: {ip}")
        
        with geoip2.database.Reader(db_path) as reader:
            response = reader.city(ip)
            city = response.city.name or 'Не определено'
            country = response.country.name or 'Не определено'
            logger.info(f"🌍 {ip} → {city}, {country}")
            return city, country
    except Exception as e:
        logger.error(f"🌍 GeoIP ОШИБКА для {ip}: {e}")
        return 'Не определено', 'Не определено'