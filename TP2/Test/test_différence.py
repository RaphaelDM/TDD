from TP2.difference import maximum

class TestMaximun:
    def test_maximum_retourne_a_si_superieur(self):
        #moke values (arrange)
        a = 5
        b = 3
        #act
        result = maximum(a, b)
        #assert
        assert result == a
        
    def test_maximun_retourne_b_si_superieur(self):
        #moke values (arrange)
        a = 4
        b = 4
        #act
        result = maximum(a, b)  
        #assert
        assert result == a
        
    def test_maximun_retourne_a_si_egale(self):
        #moke values (arrange)
        a = 7
        b = 7
        #act
        result = maximum(a, b)  
        #assert
        assert result == a



