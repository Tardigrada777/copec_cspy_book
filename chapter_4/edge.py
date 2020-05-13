from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Edge:
    u: int # вершина "откуда"
    v: int # вершина "куда"

    def reversed(self) -> Edge:
        return Edge(self.v, self.u)

    def __str__(self) -> str:
        return f'{self.u} -> {self.v}'