from typing import Any, Iterable


class DisjointSet:
    """Disjoint Set"""

    def __init__(self, elements: Iterable[str]):
        self.parent = {element: element for element in elements}

    def find(self, element: str) -> str:
        """Find element"""
        if self.parent[element] == element:
            return element
        self.parent[element] = self.find(self.parent[element])
        return self.parent[element]

    def union(self, element1: str, element2: str) -> None:
        """Union the elements"""
        root1 = self.find(element1)
        root2 = self.find(element2)
        if root1 != root2:
            self.parent[root2] = root1
