"""
Модуль генерации случайных надёжных паролей.

Используем модуль `secrets`, а не `random` — это важно для инфобеза:
`random` не криптографически стойкий генератор, его последовательность
можно предсказать. `secrets` использует источник случайности ОС
и подходит для генерации паролей, токенов и ключей.
"""

import secrets
import string


def generate_password(
    length: int = 16,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_special: bool = True,
) -> str:
    alphabet = ""
    if use_lower:
        alphabet += string.ascii_lowercase
    if use_upper:
        alphabet += string.ascii_uppercase
    if use_digits:
        alphabet += string.digits
    if use_special:
        alphabet += "!@#$%^&*()-_=+[]{}"

    if not alphabet:
        raise ValueError("Нужно выбрать хотя бы один тип символов")

    if length < 4:
        raise ValueError("Длина пароля должна быть не меньше 4 символов")

    guaranteed = []
    if use_lower:
        guaranteed.append(secrets.choice(string.ascii_lowercase))
    if use_upper:
        guaranteed.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        guaranteed.append(secrets.choice(string.digits))
    if use_special:
        guaranteed.append(secrets.choice("!@#$%^&*()-_=+[]{}"))

    remaining_length = length - len(guaranteed)
    rest = [secrets.choice(alphabet) for _ in range(remaining_length)]

    password_chars = guaranteed + rest
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)