import pytest
from qz import *


@pytest.fixture
def sample():
    return {
        'empty': (),
        'digit': (1, 2, 3),
        'digit_str': (1, 'text'),
    }


@pytest.fixture
def get_deques(sample):
    return {k: Deque(v) for k, v in sample.items()}


@pytest.fixture
def get_fifoqueues(sample):
    return {k: FIFOQueue(v) for k, v in sample.items()}


@pytest.fixture
def get_lifoqueues(sample):
    return {k: LIFOQueue(v) for k, v in sample.items()}


class TestDeque:
    def test_init(self, capsys, get_deques):
        print(get_deques['digit'])
        captured = capsys.readouterr()
        assert captured.out == 'Deque(1, 2, 3)\n'

        print(get_deques['digit_str'])
        captured = capsys.readouterr()
        assert captured.out == "Deque(1, 'text')\n"

    def test_len(self, get_deques):
        assert len(get_deques['digit']) == 3
        assert len(get_deques['digit_str']) == 2
        assert len(get_deques['empty']) == 0

    def test_append(self, capsys, get_deques):
        get_deques['digit'].append('new')
        assert len(get_deques['digit']) == 4

        print(get_deques['digit'])
        captured = capsys.readouterr()
        assert captured.out == "Deque(1, 2, 3, 'new')\n"

    def test_empty_append(self, capsys, get_deques):
        get_deques['empty'].append('new')
        assert len(get_deques['empty']) == 1

        print(get_deques['empty'])
        captured = capsys.readouterr()
        assert captured.out == "Deque('new')\n"

    def test_pop(self, capsys, get_deques):
        assert get_deques['digit'].pop() == 3
        print(get_deques['digit'])
        captured = capsys.readouterr()
        assert captured.out == "Deque(1, 2)\n"

        assert get_deques['digit_str'].pop() == 'text'
        assert get_deques['digit_str'].pop() == 1
        assert len(get_deques['digit_str']) == 0

        with pytest.raises(IndexError):
            get_deques['empty'].pop()

    def test_append_left(self, capsys, get_deques):
        get_deques['digit'].append_left(0)
        print(get_deques['digit'])
        captured = capsys.readouterr()
        assert captured.out == 'Deque(0, 1, 2, 3)\n'

        get_deques['digit_str'].append_left('left')
        print(get_deques['digit_str'])
        captured = capsys.readouterr()
        assert captured.out == "Deque('left', 1, 'text')\n"

    def test_empty_append_left(self, capsys, get_deques):
        get_deques['empty'].append_left(0)
        print(get_deques['empty'])
        captured = capsys.readouterr()
        assert captured.out == "Deque(0)\n"

        get_deques['empty'].append_left('left')
        print(get_deques['empty'])
        captured = capsys.readouterr()
        assert captured.out == "Deque('left', 0)\n"

    def test_pop_left(self, capsys, get_deques):
        assert get_deques['digit'].pop_left() == 1

        print(get_deques['digit'])
        captured = capsys.readouterr()
        assert captured.out == "Deque(2, 3)\n"

        get_deques['digit_str'].pop_left()
        assert get_deques['digit_str'].pop_left() == 'text'

        print(get_deques['digit_str'])
        captured = capsys.readouterr()
        assert captured.out == "Deque()\n"

        with pytest.raises(IndexError):
            get_deques['empty'].pop_left()

    def test_reverse(self, capsys, get_deques):
        get_deques['digit'].reverse()
        print(get_deques['digit'])
        captured = capsys.readouterr()
        assert captured.out == "Deque(3, 2, 1)\n"
        assert get_deques['digit'].pop() == 1
        assert get_deques['digit'].pop_left() == 3

        get_deques['digit_str'].reverse()
        print(get_deques['digit_str'])
        captured = capsys.readouterr()
        assert captured.out == "Deque('text', 1)\n"
        assert get_deques['digit_str'].pop_left() == 'text'
        assert get_deques['digit_str'].pop() == 1
        assert len(get_deques['digit_str']) == 0

    def test_iteration(self, get_deques):
        i = iter(get_deques['digit'])
        assert next(i) == 3
        assert next(i) == 2
        assert next(i) == 1
        with pytest.raises(StopIteration):
            assert next(i)

        assert [_ for _ in get_deques['digit']] == [3, 2, 1]

    def test_copy(self, get_deques):
        copy = get_deques['digit'].copy()
        assert get_deques['digit'] == copy
        assert get_deques['digit'] is get_deques['digit']
        assert get_deques['digit'] is not copy

    def test_as_list(self, get_deques):
        assert get_deques['digit'].as_list() == [1, 2, 3]
        assert get_deques['digit'].as_list(reverse=True) == [3, 2, 1]

    def test_max_len(self, sample, get_deques):
        assert get_deques['digit'].max_len() is None
        deq = Deque(sample['digit'], max_len=2)
        assert len(deq) == 2
        with pytest.raises(IndexError):
            deq.append('element over max length')


class TestFIFOQueue:
    def test_append(self, capsys, get_fifoqueues):
        get_fifoqueues['digit'].append('very last')
        print(get_fifoqueues['digit'])
        captured = capsys.readouterr()
        assert captured.out == "FIFOQueue(1, 2, 3, 'very last')\n"

        get_fifoqueues['empty'].append('foo')
        assert len(get_fifoqueues['empty']) == 1

        get_fifoqueues['empty'].append('bar')
        print(get_fifoqueues['empty'])
        captured = capsys.readouterr()
        assert captured.out == "FIFOQueue('foo', 'bar')\n"

    def test_pop(self, capsys, get_fifoqueues):
        assert get_fifoqueues['digit'].pop() == 1
        assert get_fifoqueues['digit'].pop() == 2
        assert get_fifoqueues['digit'].pop() == 3
        assert len(get_fifoqueues['digit']) == 0

        assert get_fifoqueues['digit_str'].pop() == 1
        print(get_fifoqueues['digit_str'])
        captured = capsys.readouterr()
        assert captured.out == "FIFOQueue('text')\n"

    def test_iteration(self, get_fifoqueues):
        i = iter(get_fifoqueues['digit'])
        assert next(i) == 1
        assert next(i) == 2
        assert next(i) == 3
        with pytest.raises(StopIteration):
            assert next(i)

    def test_restricted_methods(self, get_fifoqueues):
        assert hasattr(get_fifoqueues['digit'], 'pop_left') is False
        assert hasattr(get_fifoqueues['digit'], 'append_left') is False

        with pytest.raises(AttributeError):
            get_fifoqueues['digit_str'].append_left()
            get_fifoqueues['digit_str'].pop_left()

    def test_reverse(self, get_fifoqueues):
        get_fifoqueues['digit'].reverse()
        assert get_fifoqueues['digit'].as_list() == [3, 2, 1]

    def test_as_list(self, get_fifoqueues):
        assert get_fifoqueues['digit'].as_list() == [1, 2, 3]
        assert get_fifoqueues['digit'].as_list(reverse=True) == [3, 2, 1]


class TestLIFOQueue:
    def test_append(self, capsys, get_lifoqueues):
        get_lifoqueues['digit'].append('very first')
        print(get_lifoqueues['digit'])
        captured = capsys.readouterr()
        assert captured.out == "LIFOQueue(1, 2, 3, 'very first')\n"

        get_lifoqueues['empty'].append('foo')
        assert len(get_lifoqueues['empty']) == 1

        get_lifoqueues['empty'].append('bar')
        print(get_lifoqueues['empty'])
        captured = capsys.readouterr()
        assert captured.out == "LIFOQueue('foo', 'bar')\n"

    def test_pop(self, capsys, get_lifoqueues):
        assert get_lifoqueues['digit'].pop() == 3
        assert get_lifoqueues['digit'].pop() == 2
        assert get_lifoqueues['digit'].pop() == 1
        assert len(get_lifoqueues['digit']) == 0

        assert get_lifoqueues['digit_str'].pop() == 'text'
        print(get_lifoqueues['digit_str'])
        captured = capsys.readouterr()
        assert captured.out == "LIFOQueue(1)\n"

    def test_restricted_methods(self, get_lifoqueues):
        assert hasattr(get_lifoqueues['digit'], 'pop_left') is False
        assert hasattr(get_lifoqueues['digit'], 'append_left') is False

        with pytest.raises(AttributeError):
            get_lifoqueues['digit_str'].append_left()
            get_lifoqueues['digit_str'].pop_left()
