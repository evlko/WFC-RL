from typing import Dict, List

from project.utils.rectangulator import Rect


class GraphBuilder:
    @staticmethod
    def build_graph(rectangles: List[Rect]) -> Dict[Rect, List[Rect]]:
        graph = {rect: [] for rect in rectangles}
        for i, rect1 in enumerate(rectangles):
            for j, rect2 in enumerate(rectangles):
                if i != j and rect1.touches(
                    rect2
                ):
                    graph[rect1].append(rect2)

        return graph
