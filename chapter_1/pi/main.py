# pi = 3.14159...
# по формуле Лейбница следующий бесконечный ряд сходится к pi
# pi = 4/1 - 4/3 + 4/5 - 4/7 + 4/9 - 4/11 ...

# простое решение
# чем больше проходов, тем выше точность
def calculate_pi(n_terms: int) -> float:
    numenator: float = 4.0
    denominator: float = 1.0
    operation: float = 1.0
    pi: float = 0.0

    for _ in range(n_terms):
        pi += (numenator / denominator) * operation
        denominator += 2
        operation *= -1

    return pi

if __name__ == '__main__':
    print(calculate_pi(10000000))