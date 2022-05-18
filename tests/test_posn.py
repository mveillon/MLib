from src import Posn

def posn():
    assert str(Posn(5, 4)) == '(5, 4)'
    assert str(Posn(0, 0)) == '(0, 0)'
    assert str(Posn(-1, -2)) == '(-1, -2)'

    assert Posn(3, 3) == Posn(3, 3)
    assert Posn(3, 2) != Posn(4, 3)
    assert Posn(5, 1) > Posn(4, 3)
    assert Posn(2, 9) < Posn(9, 2)
    assert not Posn(5, 4) > Posn(5, 4)
    assert not Posn(5, 4) < Posn(5, 4)
    assert Posn(5, 4) >= Posn(5, 4)
    assert Posn(5, 4) <= Posn(5, 4)
    
    assert Posn(3, 4).distance(Posn(0, 0)) == '5'
    assert Posn(5, 5).distance(Posn(5, 5)) == '0'
    assert Posn(1, 3).distance(Posn(8, 5)) == '√53'
