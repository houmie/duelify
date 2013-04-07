def facebook_save(user, social_user, detail, response, *args, **kwargs):
    # Save any data on the custom fields in the user model
    #user.location = response.get('user_location')
    user.date_of_birth = response.get('user_birthday')
    user.save() 