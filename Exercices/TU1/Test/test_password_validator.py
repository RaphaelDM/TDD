from Exercices.TU1.PasswordValidator import PasswordValidator

class TestPasswordValidator:
    def test_password_respects_constraints_return_OK(self):
        validator = PasswordValidator("Str0ngP@ss!")
        is_valid, errors = validator.validate()
        assert is_valid is True
        assert errors == []
    def test_password_too_short_return_KO(self):
        validator = PasswordValidator("Shrt1!")
        is_valid, errors = validator.validate()
        assert is_valid is False
        assert "too short" in errors
    def test_password_missing_digi_return_KO(self):  
        validator = PasswordValidator("NoDigitPass!")
        is_valid, errors = validator.validate()
        assert is_valid is False
        assert "missing digit" in errors
    def test_password_missing_uppercase_return_KO(self):
        validator = PasswordValidator("nouppercase1!")
        is_valid, errors = validator.validate()
        assert is_valid is False
        assert "missing uppercase" in errors
    def test_password_missing_lowercase_return_KO(self):
        validator = PasswordValidator("NOLOWERCASE1!")
        is_valid, errors = validator.validate()
        assert is_valid is False
        assert "missing lowercase" in errors
    def test_password_missing_special(self):
        validator = PasswordValidator("NoSpecial1")
        is_valid, errors = validator.validate()
        assert is_valid is False
        assert "missing special" in errors
    def test_password_contains_space(self):
        validator = PasswordValidator("Has Space1!")
        is_valid, errors = validator.validate()
        assert is_valid is False
        assert "contains space" in errors
    def test_password_contains_username(self):
        validator = PasswordValidator("UserName1!", username="username")
        is_valid, errors = validator.validate()
        assert is_valid is False
        assert "contains username" in errors
    def test_password_none(self):
        validator = PasswordValidator(None)
        is_valid, errors = validator.validate()
        assert is_valid is False
        assert "password is None" in errors
    

