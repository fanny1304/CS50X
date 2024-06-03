from flask import redirect, render_template, session
from functools import wraps

def check_password(password):
    result = 5
    nb_char = len(password)
    nb_inf = 0
    nb_sup = 0
    nb_symbol = 0
    nb_number = 0

    if nb_char < 4 or nb_char > 10 :
        result -= 1

    alpha_inf = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    alpha_sup = []
    for letter in alpha_inf :
        alpha_sup.append(letter.upper())

    special_char = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '^', '_' , '`', '{', '|', '}', '~', "]", "[", "\\"]

    # check for lower character
    for char in password:
        for letter_inf in alpha_inf:
            if char == letter_inf:
                nb_inf += 1

    if nb_inf == 0:
        result -= 1

    # check for upper character
    for char in password:
        for letter_sup in alpha_sup:
            if char == letter_sup :
                nb_sup += 1

    if nb_sup == 0:
        result -= 1

    # check for symbol
    for char in password:
        for symbol in special_char:
            if char == symbol :
                nb_symbol += 1

    if nb_symbol == 0:
        result -= 1

    # check for number
    for char in password:
        if char.isdigit():
            nb_number += 1

    if nb_number == 0:
        result -= 1

    if result < 5 :
        return False

    else :
        return True


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None :
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def get_unique_values(dictionary):
    unique_values = []
    seen_values = []

    for value in dictionary:
        if value not in seen_values:
            unique_values.append(value)
            seen_values.append(value)

    return unique_values

def get_number_items(dictionary):
    number = 0
    for value in dictionary["list"] :
        number += 1

    return number