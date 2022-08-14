"""
Queues collection version 1.0
"""


class Deque:
    """
    Double ended queue.
    """
    def __copy__(self):
        return self.__class__(self.as_list())

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __init__(self, iterable=(), max_len=None):
        self._max_len = int(max_len) if max_len else None
        self._elements = {i: iterable[i] for i in range(min(len(iterable),
                                                            self._max_len if self._max_len else float('inf')
                                                            )
                                                        )
                          }
        self._head = 0 if iterable else None

    def __iter__(self):
        return iter(self.as_list(reverse=True))

    def __len__(self):
        return len(self._elements)

    def __repr__(self):
        return f"{self.__class__.__name__}([{', '.join(map(repr, self.as_list()))}])"

    def __str__(self):
        return f"{self.__class__.__name__}({', '.join(map(repr, self.as_list()))})"

    def append(self, el):
        if self.__len__() >= (self.max_len() or float('inf')):
            raise IndexError(f'{self.__class__.__name__} is full')

        if self._head is None:
            self._head = 0

        self._elements[self._head + self.__len__()] = el

    def append_left(self, el):
        if self.__len__() >= (self.max_len() or float('inf')):
            raise IndexError(f'{self.__class__.__name__} is full')

        self._head = self._head - 1 if self._head is not None else 0
        self._elements[self._head] = el

    def clear(self):
        self._elements = {}
        self._head = None

    def copy(self):
        return self.__copy__()

    def max_len(self):
        return self._max_len

    def pop(self):
        if self._head is None:
            raise IndexError(f'{self.__class__.__name__} is empty')

        if (length := self.__len__()) == 1:
            self._head, cur_head = None, self._head
            return self._elements.pop(cur_head)
        else:
            return self._elements.pop(self._head + length - 1)

    def pop_left(self):
        if self._head is None:
            raise IndexError(f'{self.__class__.__name__} is empty')

        cur_head = self._head
        self._head = None if self.__len__() == 1 else self._head + 1

        return self._elements.pop(cur_head)

    def reverse(self):
        if length := self.__len__():
            max_index = self._head + length - 1
            for i in range(length//2):
                self._elements[self._head + i], self._elements[max_index - i] = \
                    self._elements[max_index - i], self._elements[self._head + i]

    def as_list(self, reverse=False):
        return [t[1] for t in sorted(self._elements.items(), reverse=reverse)]


class FIFOQueue(Deque):
    """
    First in first out queue.
    """
    pop_left = property()
    append_left = property()

    def __iter__(self):
        return iter(self.as_list())

    def pop(self):
        return super().pop_left()


class LIFOQueue(Deque):
    """
    Last in first out queue.
    """
    pop_left = property()
    append_left = property()

