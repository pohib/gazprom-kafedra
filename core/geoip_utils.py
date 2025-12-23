import geoip2.database
import os
from django.conf import settings

def get_location_from_ip(ip):
    try:
        db_path = getattr(settings, 'GEOIP_PATH', None)
        if not db_path or not os.path.exists(db_path):
            return 'Не определено', 'Не определено'
        
        with geoip2.database.Reader(db_path) as reader:
            response = reader.city(ip)
            city = response.city.name or 'Не определено'
            country = response.country.name or 'Не определено'
            return city, country
    except Exception:
        return 'Не определено', 'Не определено'
