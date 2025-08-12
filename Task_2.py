"""Задача 2: Проверка сбалансированности скобок с использованием стека из задачи 1.

Считывает строку со стандартного ввода и печатает:
 - "Сбалансированно", если скобки корректны;
 - "Несбалансированно" — иначе.
"""

from __future__ import annotations

import sys
from typing import Dict

from Task_1 import Stack


OPENING = "([{"
CLOSING = ")]}"
PAIR_MAP: Dict[str, str] = {
    ')': '(',
    ']': '[',
    '}': '{',
}


def is_balanced(brackets: str) -> bool:
    """Проверить, является ли строка со скобками сбалансированной."""
    stack: Stack[str] = Stack()
    for char in brackets:
        if char in OPENING:
            stack.push(char)
        elif char in CLOSING:
            if stack.is_empty():
                return False
            if stack.pop() != PAIR_MAP[char]:
                return False
        else:
            # Игнорируем все не-скобочные символы, чтобы функция была устойчивой
            continue
    return stack.is_empty()


def main() -> None:
    input_data = sys.stdin.read().strip()
    print("Сбалансированно" if is_balanced(input_data) else "Несбалансированно")


if __name__ == "__main__":
    main()


