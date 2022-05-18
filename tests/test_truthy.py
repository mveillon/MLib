from src import is_truthy

def test_truthy():
    assert is_truthy(1)
    assert not is_truthy(0)
    assert is_truthy('a')
    assert not is_truthy('')
    assert is_truthy([0])
    assert not is_truthy([])
