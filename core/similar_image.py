from functools import lru_cache
import os
from typing import Dict, List
from PIL import Image

from imagehash import ImageHash

class SimilarImage:
    def __init__(self, image_path: str, image_hash: ImageHash):
        self.image_path = image_path
        self.image_hash = image_hash

    @property
    def image_size(self):
        file_size = os.path.getsize(self.image_path)
        units = ['bytes', 'kb', 'mb', 'gb', 'tb']
        exponents_map = {unit: i for i, unit in enumerate(units)}

        size, unit = next(((file_size / (1024 ** exp), unit) for unit, exp in exponents_map.items() if file_size / (1024 ** exp) >= 1),
                          (0, units[0]))
        return round(size, 3), unit


    @property
    @lru_cache(maxsize=20)
    def image_info(self):
        with Image.open(self.image_path) as img:
            width, height = img.size
            size, unit = self.image_size
            return {
                "dimensions": (width, height),
                "size": f"{size} {unit}",
            }
            

    def __repr__(self) -> str:
        # return f"Image(path={self.image_path}, info={self.image_info}, similar_images={self.similar_images})"
        return f"{os.path.basename(self.image_path)}"
