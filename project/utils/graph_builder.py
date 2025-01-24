import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Set

from project.utils.rectangulator import Rect


@dataclass
class Vertex:
    uid: int
    rect: Rect
    neighbors: Set[int] = field(default_factory=set)
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_serializable(self) -> Dict[str, Any]:
        data = asdict(self)
        data.pop("rect")  # Exclude the 'rect' field
        data["neighbors"] = list(self.neighbors)
        return data


@dataclass
class Graph:
    vertices: List[Vertex]

    def to_serializable(self) -> Dict[str, Any]:
        return {"vertices": [vertex.to_serializable() for vertex in self.vertices]}

    def to_json(self, filename: str) -> None:
        with open(filename, "w") as f:
            json.dump(self.to_serializable(), f, indent=4)


class GraphBuilder:
    @staticmethod
    def build_graph(rectangles: List[Rect]) -> Dict[Rect, List[Rect]]:
        graph = Graph(
            vertices=[Vertex(uid=i, rect=rect) for i, rect in enumerate(rectangles)]
        )

        for vertex1 in graph.vertices:
            vertex1.meta["area"] = vertex1.rect.area
            for vertex2 in graph.vertices:
                if (
                    vertex1.uid != vertex2.uid
                    and vertex1.rect.touches(vertex2.rect)
                    and vertex2.uid not in vertex1.neighbors
                ):
                    vertex1.neighbors.add(vertex2.uid)
                    vertex2.neighbors.add(vertex1.uid)

        return graph
