from typing import List, Tuple, Optional

class PasswordValidator:
    def __init__(self, password: str, username: Optional[str] = None):
        self.password = password
        self.username = username

    def validate(self) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        password = self.password
        username = self.username

        if password is None:
            errors.append("password is None")
            return False, errors

        if len(password) < 8:
            errors.append("too short")
        if not any(char.isdigit() for char in password):
            errors.append("missing digit")
        if not any(char.isupper() for char in password):
            errors.append("missing uppercase")
        if not any(char.islower() for char in password):
            errors.append("missing lowercase")
        if not any(char in "!@#$%^&*()-_+=" for char in password):
            errors.append("missing special")
        if ' ' in password:
            errors.append("contains space")
        if username and username.strip() != '' and username.lower() in password.lower():
            errors.append("contains username")

        return (len(errors) == 0), errors
    
    def get_strength(self) -> str:
        is_valid, errors = self.validate()
        if not is_valid:
            return "Refuser"
        length = len(self.password)
        if length >= 12:
            return "Fort"
        elif length >= 8:
            return "Moyen"
        else:
            return "Faible"
