from datetime import datetime

def facebook_save(user, social_user, details, response, *args, **kwargs):
    dob = response.get('birthday')
    if dob:
        user.date_of_birth = datetime.strptime(response.get('birthday'), '%m/%d/%Y')        
        user.save()       
