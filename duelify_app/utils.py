from datetime import datetime
from django.contrib.gis.geoip import GeoIP
from collections import namedtuple


def social_media_save(request, user, social_user, details, response, *args, **kwargs):
    dob = None
    loc = None    
    if not user.date_of_birth:
        if 'birthday' in response:
            dob = response.get('birthday')
            try: # facebook
                user.date_of_birth = datetime.strptime(dob, '%m/%d/%Y')
            except:
                try:
                    # google
                    user.date_of_birth = datetime.strptime(dob, '%Y-%m-%d')
                except:
                    pass
    
    if not user.location:
        if 'location' in response:
            try: # facebook
                loc = response.get('location').get('name')
            except: #twitter
                loc = response.get('location')
        if not loc: # Last resort through IP                    
            loc = get_user_location_details(request).country
        user.location = loc
        
    browser_type = get_user_browser(request)            
    user.browser = browser_type
    
    user.save()
    



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_location_details(request):
    g = GeoIP()
    ip=get_client_ip(request)
    country = ''
    
    if ip:
        try:
            country = g.country(ip)['country_name']
        except TypeError:
            pass
    
    Result = namedtuple("result", ["country", "ip"])
    return Result(country=country, ip=ip)
    

def get_user_browser(request):
    browser_type = ''
    if 'HTTP_USER_AGENT' in request.META:
        browser_type = request.META['HTTP_USER_AGENT']
    return browser_type