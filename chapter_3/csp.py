from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractclassmethod

V = TypeVar('V') # тип variable для переменной
D = TypeVar('D') # тип domain для области определений

# базовый класс для всех ограничений
class Constraint(Generic[V, D], ABC):
    # переменные, для которых существует ограничение
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    # необходимо переопределить в подклассах
    @abstractclassmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        pass

# задача с ограничениями состоит из переменных типа V
# которые имеют диапазоны значений, известные как области определения
# типа D и ограничений, которые определяют, является ли допустимым
# выбор данной области определения для данной переменной
class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables # переменные, которые будут ограничены 
        self.domains: Dict[V, List[D]] = domains # домен (обл определения) каждой переменной
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError('Every variable should have a domain assigned to it.')

    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError('Variable in constraint not in CSP!')
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        # присваивание завершено, если существует присваивание
        # для каждой переменной (базовый случай)
        if len(assignment) == len(self.variables):
            return assignment

        # получить все переменные из CSP, но не из присваивания
        unassigned: List[V] = [v for v in self.variables if v not in assignment]

        # получить все возможные значения области определения
        # для первой переменной без присваивания
        first: V = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            # если нет противоречий, продолжаем рекурсию
            if self.consistent(first, local_assignment):
                result: Optional[Dict[V, D]] = self.backtracking_search(local_assignment)
                # если результат не найден, заканчиваем возвраты
                if result is not None:
                    return result
        return None
