from greyspace import settings
import requests


# get country with ip address from ipinfo.io
def get_ip_address_info(ip_address):
    address = '154.160.14.80' if ip_address == '127.0.0.1' else ip_address
    url = "https://ipinfo.io/%s?token=%s" % (address, settings.IPINFO_TOKEN)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def verify_google_recaptcha(request):
    """Verify google recaptcha"""
    url = 'https://www.google.com/recaptcha/api/siteverify'
    captcha_token = request.POST.get('g-recaptcha-response')
    payload = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': captcha_token
    }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return None
