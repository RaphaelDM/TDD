from TP1.carre import Math

carre = Math.carre
addition = Math.addition


print("Carre tests")
class TestCarre:
    def test_carre_de_2(self):
        assert carre(2) == 4

    def test_carre_de_0(self):
        assert carre(0) == 0

    def test_carre_de_negatif(self):
        assert carre(-3) == 9
    
    def test_carre_de_string(self):
        try:
            carre("2")
            assert False
        except TypeError:
            assert True
    def test_carre_de_float(self):
        assert carre(2.5) == 6.25 


