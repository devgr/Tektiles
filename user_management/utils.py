def password_meets_complexity(pw):
    if len(pw) < 6:
        return 'Password must be at least 6 characters long'

    if not any(c.isupper() or c.isdigit() for c in pw):
        return 'Password must contain at least one capital letter or number'

    return True
