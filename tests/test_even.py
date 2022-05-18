from src import even, odd

def test_even():
    for i in range(-100, 100):
        if i % 2 == 0:
            assert even(i)
            assert not odd(i)
        else:
            assert odd(i)
            assert not even(i)
