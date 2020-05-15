from typing import TypeVar, List, Optional
from weighted_graph import WeightedGraph
from weighted_edge import WeightedEdge
from priority_queue import PriorityQueue

V = TypeVar('V') # тип вершин в графе
WeightedPath = List[WeightedEdge] # псевдоним для типа путей

def total_weight(wp: WeightedPath) -> float:
    return sum([e.weight for e in wp])

def mst(wg: WeightedGraph[V], start: int = 0) -> Optional[WeightedPath]:
    if start > (wg.vertex_count - 1) or start < 0:
        return None

    result: WeightedPath = [] # содержит окончательное MST
    pq: PriorityQueue[WeightedEdge] = PriorityQueue()
    visited: [bool] = [False] * wg.vertex_count # здесь мы уже были

    def visit(index: int):
        visited[index] = True # пометить как прочитанное
        for edge in wg.edges_for_index(index):
            # добавляем все ребра отсюда в pq
            if not visited[edge.v]:
                pq.push(edge)

    visit(start) # первая вершина, с которой все начинается

    while not pq.empty: # продолжаем пока есть необработанные вершины
        edge = pq.pop()
        if visited[edge.v]:
            continue # чтобы никогда не просмотреть второй раз
        # на данный момент это минимальный вес, поэтому добавляем в дерево
        result.append(edge)
        # идем дальше
        visit(edge.v)
    return result

    
def print_weighted_graph(wg: WeightedGraph, wp: WeightedPath) -> None:
    for edge in wp:
        print(f'{wg.vertex_at(edge.u)} {edge.weight} --> {wg.vertex_at(edge.v)}')
    print(f'Total weight: {total_weight(wp)}')

if __name__ == '__main__':
    city_graph2: WeightedGraph[str] = WeightedGraph(['Seattle', 'San Francisco', 'Los Angeles', 'Riverside', 'Phoenix', 'Chicago', \
        'Boston', 'New York', 'Atlanta', 'Miami', 'Dallas', 'Houston', 'Detroit', 'Philadelphia', 'Washington'])
    city_graph2.add_edge_by_vertices('Seattle', 'Chicago', 1737)
    city_graph2.add_edge_by_vertices('Seattle', 'San Francisco', 678)
    city_graph2.add_edge_by_vertices('San Francisco', 'Riverside', 386)
    city_graph2.add_edge_by_vertices('San Francisco', 'Los Angeles', 348)
    city_graph2.add_edge_by_vertices('Los Angeles', 'Riverside', 50)
    city_graph2.add_edge_by_vertices('Los Angeles', 'Phoenix', 357)
    city_graph2.add_edge_by_vertices('Riverside', 'Phoenix', 307)
    city_graph2.add_edge_by_vertices('Riverside', 'Chicago', 1704)
    city_graph2.add_edge_by_vertices('Phoenix', 'Dallas', 887)
    city_graph2.add_edge_by_vertices('Phoenix', 'Houston', 1015)
    city_graph2.add_edge_by_vertices('Dallas', 'Chicago', 805)
    city_graph2.add_edge_by_vertices('Dallas', 'Atlanta', 721)
    city_graph2.add_edge_by_vertices('Dallas', 'Houston', 225)
    city_graph2.add_edge_by_vertices('Houston', 'Atlanta', 702)
    city_graph2.add_edge_by_vertices('Houston', 'Miami', 968)
    city_graph2.add_edge_by_vertices('Atlanta', 'Chicago', 588)
    city_graph2.add_edge_by_vertices('Atlanta', 'Washington', 543)
    city_graph2.add_edge_by_vertices('Atlanta', 'Miami', 604)
    city_graph2.add_edge_by_vertices('Miami', 'Washington', 923)
    city_graph2.add_edge_by_vertices('Chicago', 'Detroit', 238)
    city_graph2.add_edge_by_vertices('Detroit', 'Boston', 613)
    city_graph2.add_edge_by_vertices('Detroit', 'Washington', 396)
    city_graph2.add_edge_by_vertices('Detroit', 'New York', 482)
    city_graph2.add_edge_by_vertices('Boston', 'New York', 190)
    city_graph2.add_edge_by_vertices('New York', 'Philadelphia', 81)
    city_graph2.add_edge_by_vertices('Philadelphia', 'Washington', 123)

    result: Optional[WeightedPath] = mst(city_graph2)

    if result is None:
        print('No solution found!')
    else:
        print_weighted_graph(city_graph2, result)


