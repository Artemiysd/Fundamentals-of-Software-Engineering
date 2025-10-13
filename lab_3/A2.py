import string

password = input('введите пароль')
allowed = string.ascii_uppercase + string.ascii_lowercase + string.digits + '*-#'
has_upper = any(c.isupper() for c in password)
has_lower = any(c.islower() for c in password)
has_digit = any(c.isdigit() for c in password)
has_special = any( c in '*-#' for c in password)
all_lowed = all(c in allowed for c in password)
if len(password) != 8:
    print('длина пароля не равна 8')
if not has_upper:
    print('отсутствуют заглавные буквы')
if not has_lower:
    print('отсутствуют строчные буквы')
if not has_digit:
    print('отсутствуют цифры')
if not has_special:
    print('отсутствуют специальные символы')
if not all_lowed:
    print('в пароле используються непредусмотренные символы')
