from TP1.carre import Math

division = Math.division

class TestDivision:
    def test_division_10_2(self):
        assert Math.division(10,2) == 5
    def test_division_par_0(self):
        try:
            division(10,0)
            assert False
        except ZeroDivisionError:
            assert True
    def test_division_float(self):
        assert division(7.5,2.5) == 3.0
    
    def test_division_negatif(self):
        assert division(-10,2) == -5
        
    def test_division_string(self):
        try:
            division("10",2)
            assert False
        except TypeError:
            assert True    
        
        