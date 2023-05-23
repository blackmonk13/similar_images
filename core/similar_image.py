from functools import lru_cache
import os
from typing import Dict, List
from PIL import Image
from math import gcd

from imagehash import ImageHash

class SimilarImage:
    def __init__(self, image_path: str, image_hash: ImageHash):
        self.image_path = image_path
        self.image_hash = image_hash
        self.similar_images:Dict[int, List[SimilarImage]] = {}  # Initialize an empty dictionary
        
    def compare_hash(self, other_path:str, other_hash: ImageHash, threshold: int):
        similarity = self.image_hash - other_hash
        if similarity in self.similar_images:
            self.similar_images[similarity]
        
    # def add_similar_image(self, similar_image_path: str, similarity_difference: int):
    #     # Images with the same similarity difference should be grouped together
    #     if similarity_difference in self.similar_images:
    #         self.similar_images[similarity_difference].append(similar_image_path)
    #     else:
    #         self.similar_images[similarity_difference] = [similar_image_path]
        
    @staticmethod
    def get_aspect_ratio(width: int, height: int) -> tuple[int, int]:
        divisor = gcd(width, height)  # type: ignore
        return width // divisor, height // divisor

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
            aspect_ratio = self.get_aspect_ratio(width, height)
            
            size, unit = self.image_size
            return {
                "dimensions": (width, height),
                "size": f"{size} {unit}",
                "aspect_ratio": f"{aspect_ratio[0]} / {aspect_ratio[1]}",
            }
            
    # def remove_similarity(self, image_path: str):
    #     for similar_image in self.similar_images:
    #         for similarity_difference, image_paths in similar_image.similar_images.items():
    #             if image_path in image_paths:
    #                 image_paths.remove(image_path)
    #                 # If the list for the similarity_difference is empty, remove the key from the dictionary
    #                 if not image_paths:
    #                     del similar_image.similar_images[similarity_difference]
    #                 break

    def __repr__(self) -> str:
        # return f"Image(path={self.image_path}, info={self.image_info}, similar_images={self.similar_images})"
        return f"{os.path.basename(self.image_path)}"
