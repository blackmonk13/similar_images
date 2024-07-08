"""
Initialize the package
"""

import sys
import os

from .similarity_finder import SimilarityFinder
from .similar_image import SimilarImage
from .disjoint_set import DisjointSet

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

__all__ = [
    "SimilarityFinder",
    "SimilarImage",
    "DisjointSet",
]
