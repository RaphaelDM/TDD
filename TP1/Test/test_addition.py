from TP1.carre import Math

addition= Math.addition


print("Addition tests") 
class Testaddiditional:
    def test_adition_5(self):
        assert addition(5,10) == 15
        
    def test_addition_negatif(self):
        assert addition(-5,10) == 5
        
    def test_addition_float(self):
        assert addition(2.5,3.5) == 6.0
    def test_addition_string(self):
        try:
            addition("5",10)
            assert False
        except TypeError:
            assert True
    def test_addition_zero(self):
        assert addition(0,0) == 0
    def test_addition_grand_nombre(self):
        assert addition(1_000_000,2_000_000) == 3_000_000
        
    def test_addition_negatif_et_float(self):
        assert addition(-2.5,3.5) == 1.0
    def test_addition_multiple(self):
        assert addition(addition(2,3),addition(4,5)) == 14
        