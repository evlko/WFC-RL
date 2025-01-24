import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Set

import networkx as nx

from project.utils.rectangulator import Rect


@dataclass
class Vertex:
    uid: int
    rect: Rect
    neighbors: Set[int] = field(default_factory=set)

    def to_serializable(self) -> Dict[str, Any]:
        data = asdict(self)
        data.pop("rect")
        data["neighbors"] = list(self.neighbors)
        return data


@dataclass
class Graph:
    vertices: Dict[int, Vertex]

    @staticmethod
    def create_nx_graph(vertices: Dict[int, Vertex]) -> nx.Graph:
        G = nx.Graph()

        for uid in vertices.keys():
            G.add_node(uid)

        for uid, vertex in vertices.items():
            for neighbor in vertex.neighbors:
                if G.has_edge(uid, neighbor):
                    continue
                G.add_edge(uid, neighbor)

        return G

    def calculate_features(self):
        G = self.create_nx_graph(self.vertices)
        num_nodes = len(self.vertices)
        num_edges = (
            sum(len(self.vertices[vertex].neighbors) for vertex in self.vertices) // 2
        )
        avg_degree = (
            sum(len(self.vertices[vertex].neighbors) for vertex in self.vertices)
            / num_nodes
        )
        avg_area = round(
            (
                sum(self.vertices[vertex].rect.area for vertex in self.vertices)
                / num_nodes
            ),
            2,
        )
        clustering_coeff = round(nx.average_clustering(G), 2)
        diameter = nx.diameter(G) if nx.is_connected(G) else "Infinity"
        avg_path_length = (
            nx.average_shortest_path_length(G) if nx.is_connected(G) else "Infinity"
        )
        largest_component = max(len(c) for c in nx.connected_components(G))
        density = nx.density(G)
        num_cliques = len(list(nx.find_cliques(G)))
        triangle_counts = nx.triangles(G)
        avg_triangles = sum(triangle_counts.values()) / len(triangle_counts)

        return (
            {
                "num_nodes": num_nodes,
                "num_edges": num_edges,
                "avg_degree": avg_degree,
                "clustering_coeff": clustering_coeff,
                "diameter": diameter,
                "avg_path_length": avg_path_length,
                "avg_area": avg_area,
                "largest_component": largest_component,
                "density": density,
                "num_cliques": num_cliques,
                "triangles": avg_triangles,
            },
        )

    def to_serializable(self) -> Dict[str, Any]:
        meta = self.calculate_features()

        return {
            "meta": meta,
            "vertices": {
                uid: vertex.to_serializable() for uid, vertex in self.vertices.items()
            },
        }

    def to_json(self, filename: str) -> None:
        with open(filename, "w") as f:
            json.dump(self.to_serializable(), f, indent=4)
