import traceback
from uwsgi_tasks import task, TaskExecutor

from .dataclasses import IPInfo
from .utils import get_ip_address_info


@task(executor=TaskExecutor.SPOOLER)
def update_page_ipinfo(page):
    """Get ipinfo for a given ip address."""
    try:
        ip_info = get_ip_address_info(page.ip_address)

        if not ip_info:
            return

        ip_info_data = IPInfo(
            ip=ip_info.get('ip'),
            country=ip_info.get('country'),
            city=ip_info.get('city'),
            region=ip_info.get('region'),
            loc=ip_info.get('loc'),
            org=ip_info.get('org'),
            timezone=ip_info.get('timezone'),
            hostname=ip_info.get('hostname')
        )
        location_lat, location_lng = tuple(ip_info_data.loc.split(","))

        page.update(
            country=ip_info_data.country,
            city=ip_info_data.city,
            location_lat=location_lat,
            location_lng=location_lng,
        )

    except Exception as ex:
        st_trace = traceback.format_exc()
        log_exception(ex, st_trace)
