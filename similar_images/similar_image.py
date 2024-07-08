from functools import lru_cache
import os
from typing import Tuple, TypedDict
from PIL import Image

from imagehash import ImageHash


class ImageInfo(TypedDict):
    dimensions: Tuple[int, int]
    size: str


class SimilarImage:
    """Similar image"""

    def __init__(
        self,
        image_path: str,
        image_hash: ImageHash,
    ):
        self.image_path = image_path
        self.image_hash = image_hash

    @property
    def image_size(self):
        """Get image size in human-readable format."""
        file_size = os.path.getsize(self.image_path)
        units = ["bytes", "KB", "MB", "GB", "TB"]
        exponents_map = {unit: i for i, unit in enumerate(units)}

        size, unit = next(
            (
                (file_size / (1024**exp), unit)
                for unit, exp in exponents_map.items()
                if file_size / (1024**exp) >= 1
            ),
            (0, units[0]),
        )
        return round(size, 3), unit

    @property
    @lru_cache(maxsize=20)
    def image_info(self) -> ImageInfo:
        """Get the image info"""
        with Image.open(self.image_path) as img:
            width, height = img.size
            size, unit = self.image_size
            return {
                "dimensions": (width, height),
                "size": f"{size} {unit}",
            }

    def __repr__(self) -> str:
        return f"{os.path.basename(self.image_path)}"

    def to_dict(self):
        """Convert to dict"""
        return {
            "image_path": self.image_path,
            "image_hash": str(self.image_hash),
            "image_info": self.image_info,
        }
