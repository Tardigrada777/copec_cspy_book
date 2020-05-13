from typing import TypeVar, Generic, List, Optional
from edge import Edge
from generic_search import bfs, Node, node_to_path

V = TypeVar('V') # тип вершин графа

class Graph(Generic[V]):
    def __init__(self, vertices: List[V] = []) -> None:
        self._vertices: List[V] = vertices
        self._edges: List[List[Edge]] = [[] for _ in vertices]

    @property
    def vertex_count(self) -> int:
        return len(self._vertices) # количество вершин

    @property
    def edge_count(self) -> int:
        return sum(map(len, self._edges)) # количество ребер

    # добавляем вершину в граф и возвращаем ее индекс
    def add_vertex(self, vertex: V) -> int:
        self._vertices.append(vertex)
        self._edges.append([]) # добавляем пустой список для ребер
        return self.vertex_count - 1 # возвращаем индекс по добавленным вершинам

    # Это ненаправленный граф
    # поэтому мы всегда добавляем вершины в обоих направлениях
    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)
        self._edges[edge.v].append(edge.reversed())

    # добавляем ребро, используя индексы вершин (удобный метод)
    def add_edge_by_indices(self, u: int, v: int) -> None:
        edge: Edge = Edge(u, v)
        self.add_edge(edge)

    # добавляем ребро, просматривая индексы вершин (удобный метод)
    def add_edge_by_vertices(self, first: V, second: V) -> None:
        u: int = self._vertices.index(first)
        v: int = self._vertices.index(second)
        self.add_edge_by_indices(u, v)

    # поиск вершины по индексу
    def vertex_at(self, index: int) -> V:
        return self._vertices[index]

    # поиск индекса вершины в графе
    def index_of(self, vertex: V) -> int:
        return self._vertices.index(vertex)

    # поиск вершин, с которыми связана вершина с заданным индексом
    def neighbors_for_index(self, index: int) -> List[V]:
        return list(map(self.vertex_at, [e.v for e in self._edges[index]]))

    # поиск индекса вершины, возвращает ее соседей (удобный метод)
    def neighbors_for_vertex(self, vertex: V) -> List[V]:
        return self.neighbors_for_index(self.index_of(vertex))

    # возвращает все ребра, связанные с вершиной, имеющей заданный индекс
    def edges_for_index(self, index: int) -> List[Edge]:
        return self._edges[index]

    # поиск индекса вершины, возвращает ее ребра (удобный метод)
    def edges_for_vertex(self, vertex: V) -> List[Edge]:
        return self.edges_for_index(self.index_of(vertex))

    # упрощенный красивый вывод графа
    def __str__(self) -> str:
        desc: str = ''
        for i in range(self.vertex_count):
            desc += f'{self.vertex_at(i)} -> {self.neighbors_for_index(i)}\n'
        return desc

if __name__ == '__main__':
    # тест простейщей графовой конструкции
    city_graph: Graph[str] = Graph([
        'Seattle',
        'San Francisco',
        'Los Angeles',
        'Riverside',
        'Phoenix',
        'Chicago',
        'Boston',
        'New York',
        'Atlanta',
        'Miami',
        'Dallas',
        'Houston',
        'Detroit',
        'Philadelphia',
        'Washington'
    ])

    city_graph.add_edge_by_vertices('Seattle', 'Chicago')
    city_graph.add_edge_by_vertices('Seattle', 'San Francisco')
    city_graph.add_edge_by_vertices('San Francisco', 'Riverside')
    city_graph.add_edge_by_vertices('San Francisco', 'Los Angeles')
    city_graph.add_edge_by_vertices('Los Angeles', 'Riverside')
    city_graph.add_edge_by_vertices('Los Angeles', 'Phoenix')
    city_graph.add_edge_by_vertices('Riverside', 'Phoenix')
    city_graph.add_edge_by_vertices('Riverside', 'Chicago')
    city_graph.add_edge_by_vertices('Phoenix', 'Dallas')
    city_graph.add_edge_by_vertices('Phoenix', 'Houston')
    city_graph.add_edge_by_vertices('Dallas', 'Chicago')
    city_graph.add_edge_by_vertices('Dallas', 'Atlanta')
    city_graph.add_edge_by_vertices('Dallas', 'Houston')
    city_graph.add_edge_by_vertices('Houston', 'Atlanta')
    city_graph.add_edge_by_vertices('Houston', 'Miami')
    city_graph.add_edge_by_vertices('Atlanta', 'Chicago')
    city_graph.add_edge_by_vertices('Atlanta', 'Washington')
    city_graph.add_edge_by_vertices('Atlanta', 'Miami')
    city_graph.add_edge_by_vertices('Miami', 'Washington')
    city_graph.add_edge_by_vertices('Chicago', 'Detroit')
    city_graph.add_edge_by_vertices('Detroit', 'Boston')
    city_graph.add_edge_by_vertices('Detroit', 'Washington')
    city_graph.add_edge_by_vertices('Detroit', 'New York')
    city_graph.add_edge_by_vertices('Boston', 'New York')
    city_graph.add_edge_by_vertices('New York', 'Philadelphia')
    city_graph.add_edge_by_vertices('Philadelphia', 'Washington')

    bfs_result: Optional[Node[V]] = bfs('Boston', lambda x: x == 'Miami', city_graph.neighbors_for_vertex)
    if bfs_result is None:
        print('No solution found using beadth-first search!')
    else:
        path: List[V] = node_to_path(bfs_result)
        print('Path from Boston to Miami')
        print(path)