"""
Модуль анализа надёжности пароля.

Логика:
1. Считаем, какие типы символов есть в пароле (строчные, заглавные, цифры, спецсимволы)
2. На основе длины и разнообразия символов считаем энтропию (в битах)
3. Проверяем пароль на популярность (по небольшому встроенному списку)
4. Выдаём оценку: слабый / средний / надёжный / очень надёжный
"""

import math
import re

COMMON_PASSWORDS = {
    "123456", "123456789", "qwerty", "password", "111111",
    "12345678", "abc123", "1234567", "password1", "12345",
    "qwerty123", "1q2w3e4r", "admin", "letmein", "monkey",
    "iloveyou", "1234567890", "qazwsx", "123123", "dragon",
}


def analyze_password(password: str) -> dict:
    length = len(password)
    has_lower = bool(re.search(r"[a-zа-я]", password))
    has_upper = bool(re.search(r"[A-ZА-Я]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[^a-zA-Zа-яА-Я0-9]", password))
    is_common = password.lower() in COMMON_PASSWORDS

    pool_size = 0
    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_special:
        pool_size += 33

    entropy = length * math.log2(pool_size) if pool_size > 0 else 0.0

    tips = []
    if length < 8:
        tips.append("Увеличь длину пароля минимум до 8 символов (лучше 12+)")
    if not has_upper:
        tips.append("Добавь заглавные буквы")
    if not has_lower:
        tips.append("Добавь строчные буквы")
    if not has_digit:
        tips.append("Добавь цифры")
    if not has_special:
        tips.append("Добавь спецсимволы (!@#$% и т.д.)")
    if is_common:
        tips.append("Этот пароль есть в списках самых популярных — его точно нужно сменить")

    if is_common:
        score = 0
    elif entropy < 28:
        score = 1
    elif entropy < 45:
        score = 2
    elif entropy < 65:
        score = 3
    else:
        score = 4

    verdicts = {
        0: "🔴 Очень слабый (в списке популярных паролей)",
        1: "🔴 Слабый",
        2: "🟡 Средний",
        3: "🟢 Надёжный",
        4: "🟢 Очень надёжный",
    }

    return {
        "length": length,
        "has_lower": has_lower,
        "has_upper": has_upper,
        "has_digit": has_digit,
        "has_special": has_special,
        "entropy": round(entropy, 1),
        "is_common": is_common,
        "score": score,
        "verdict": verdicts[score],
        "tips": tips,
    }


def format_report(password: str) -> str:
    result = analyze_password(password)

    lines = [
        f"Оценка: {result['verdict']}",
        f"Длина: {result['length']} символов",
        f"Энтропия: ~{result['entropy']} бит",
        "",
        "Состав пароля:",
        f"  • строчные буквы: {'да' if result['has_lower'] else 'нет'}",
        f"  • заглавные буквы: {'да' if result['has_upper'] else 'нет'}",
        f"  • цифры: {'да' if result['has_digit'] else 'нет'}",
        f"  • спецсимволы: {'да' if result['has_special'] else 'нет'}",
    ]

    if result["tips"]:
        lines.append("")
        lines.append("Рекомендации:")
        for tip in result["tips"]:
            lines.append(f"  ⚠️ {tip}")

    return "\n".join(lines)