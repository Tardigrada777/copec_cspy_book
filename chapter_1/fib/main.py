from typing import Dict, Generator
from functools import lru_cache

# Наивное и простое решение через рекурсию
# Данное решение крайне неэффективно, так как
# при больших значениях n дерево вызовов функции
# растет в геометрической прогрессии.
# например, для fib(20) функция будет вызвана 21891 раз
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 2) + fib(n - 1)

# Оптимизация через мемоизацию
memo: Dict[int, int] = {0: 0, 1:1} # базовые случаи
def fib_with_memo(n: int) -> int:
    if n not in memo:
        memo[n] = fib(n - 1) + fib(n - 2)
    return memo[n]

# Мемоизация через lru_cache, встроенный в стандартную библиотеку
@lru_cache(maxsize=None)
def fib_lru(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 2) + fib(n - 1)

# Итеративное решение
def fib_iterative(n: int) -> int:
    if n == 0: return n # специальный случай
    last: int = 0
    next: int = 1
    for _ in range(1, n):
        last, next = next, last + next
    return next

# Решение через генератор
def fib_by_generator(n: int) -> Generator[int, None, None]:
    yield 0 # специальный случай
    if n > 0: yield 1 # если n > 0, то необходимо вывести еще один спец случай - 1
    # начинаем итерацию по числам
    last: int = 0
    next: int = 1
    for _ in range(1, n):
        last, next = next, last + next
        yield next # главный этап генерации
