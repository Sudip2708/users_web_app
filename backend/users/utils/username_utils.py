
def unique_username_check(username):
    # Vytvoření jedinečného jména z uživatelovo emailu
    pass
    # unique_username = username
    # counter = 1
    #
    # from ..custom_user import CustomUser
    # while CustomUser.objects.filter(username=unique_username).exists():
    #     username = f"{base_username}{counter}"
    #     counter += 1
    #
    # return username

def unique_username_from_email(email):
    # Vytvoření jedinečného jména z uživatelovo emailu

    base_username = email.split('@')[0].lower()
    username = base_username
    counter = 1

    from ..custom_user import CustomUser
    while CustomUser.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    return username