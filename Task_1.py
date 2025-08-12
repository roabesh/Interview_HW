"""Задача 1: Реализация стека (LIFO).

Модуль предоставляет класс `Stack` с базовыми операциями:
- проверка пустоты, добавление, удаление верхнего элемента,
- просмотр верхнего элемента без удаления,
- получение размера.
"""

from __future__ import annotations

from typing import Generic, Iterable, Iterator, List, Optional, TypeVar


T = TypeVar("T")


class Stack(Generic[T]):
    """Простой обобщённый стек (LIFO).

    Методы:
        - is_empty: вернуть True, если стек пуст.
        - push: добавить элемент на вершину стека.
        - pop: снять и вернуть верхний элемент стека.
        - peek: вернуть верхний элемент без удаления.
        - size: вернуть количество элементов в стеке.
    """

    def __init__(self, values: Optional[Iterable[T]] = None) -> None:
        self._items: List[T] = []
        if values is not None:
            for value in values:
                self._items.append(value)

    def is_empty(self) -> bool:
        """Проверить, пуст ли стек."""
        return len(self._items) == 0

    def push(self, item: T) -> None:
        """Добавить элемент на вершину стека."""
        self._items.append(item)

    def pop(self) -> T:
        """Снять и вернуть верхний элемент. Бросает IndexError, если стек пуст."""
        if self.is_empty():
            raise IndexError("pop из пустого стека")
        return self._items.pop()

    def peek(self) -> T:
        """Вернуть верхний элемент без удаления. Бросает IndexError, если стек пуст."""
        if self.is_empty():
            raise IndexError("peek из пустого стека")
        return self._items[-1]

    def size(self) -> int:
        """Вернуть количество элементов в стеке."""
        return len(self._items)

    def __len__(self) -> int:  # pragma: no cover — удобство
        return self.size()

    def __iter__(self) -> Iterator[T]:  # pragma: no cover — удобство
        return iter(self._items)

    def __repr__(self) -> str:  # pragma: no cover — удобство
        return f"Stack({self._items!r})"


if __name__ == "__main__":
    # Небольшая демонстрация при запуске файла напрямую
    sample_stack: Stack[int] = Stack()
    assert sample_stack.is_empty() is True
    sample_stack.push(1)
    sample_stack.push(2)
    sample_stack.push(3)
    assert sample_stack.size() == 3
    assert sample_stack.peek() == 3
    assert sample_stack.pop() == 3
    assert sample_stack.pop() == 2
    assert sample_stack.pop() == 1
    try:
        sample_stack.pop()
    except IndexError:
        print("Стек работает корректно (IndexError при pop из пустого стека)")
    else:
        raise AssertionError("Ожидался IndexError при pop из пустого стека")


