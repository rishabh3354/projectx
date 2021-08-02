import re


def email_validation_check(email):
    """
    for email, valid syntax returns True, else False.
    :param email:
    :return:
    """
    regex = '^[a-z0-9A-Z]+[\._]?[a-z0-9A-Z]+[@]\w+-?\w+[.]\w{2,3}$'
    if re.search(regex, email):
        return True
    else:
        return False


def check_if_password_match(password, repassword):
    if password == repassword:
        return True
    else:
        return False
