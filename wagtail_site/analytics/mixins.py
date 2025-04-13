from apps.common import is_ajax
from .models import PageVisit, Advertiser
from .tasks import update_page_ipinfo


class PageVisitLogMixin:
    def dispatch(self, request, *args, **kwargs):
        # Log the page visit
        if not is_ajax(request) and not request.user_agent.is_bot:
            page_data = {
                "path": request.path,
                "method": request.method,
                "ip_address": request.META.get('REMOTE_ADDR'),
                "user_agent": request.META.get('HTTP_USER_AGENT'),
                "referer": request.META.get('HTTP_REFERER'),
                "session_id": request.session.session_key,
            }
            # get advertising ID from request
            advert_id = request.GET.get('wds')
            if advert_id and (is_advertiser := Advertiser.objects.filter(tracking_no=advert_id)).exists():
                advertiser = is_advertiser.first()

                page_data["advertiser"] = advertiser
                page_data["advertiser_name"] = advertiser.name

            page = PageVisit.objects.create(
                **page_data
            )
            
            # Update the ipinfo
            update_page_ipinfo(page)

        return super().dispatch(request, *args, **kwargs)