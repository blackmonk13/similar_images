import itertools
import os
import threading
from PIL import Image, UnidentifiedImageError
import imagehash
import base64
import mimetypes
import tempfile
from math import gcd
from pathlib import Path
from io import BytesIO
from fractions import Fraction
from send2trash import send2trash
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Iterable, List, Tuple
from functools import lru_cache

from core.similar_image import SimilarImage


class SimilarityFinder:
    def get_image_hash(self, image_path: str) -> imagehash.ImageHash | None:
        try:
            with Image.open(image_path) as image:
                hash_value = imagehash.average_hash(image)
                return hash_value
        except UnidentifiedImageError:
            return None

    def walk_path(self, root_path: str) -> Iterable[str]:
        for root_path, directories, files in os.walk(root_path):
            for file_name in files:
                file_path = os.path.join(
                    root_path, file_name).replace("\\", "/")
                mime_type = mimetypes.guess_type(file_path)
                if mime_type[0] is not None and mime_type[0].startswith("image"):
                    yield file_path

    def find_similar_images(self, folder_dir: str, threshold: int = 10):
        images_with_hashes: set[SimilarImage] = set()
        all_files = self.walk_path(folder_dir)
        similar_images: Dict[SimilarImage, Dict[int, List[SimilarImage]]] = {}

        def process_hash(file: str):
            hash_value = self.get_image_hash(file)
            if hash_value is not None:
                return SimilarImage(file, hash_value)
            
        def group_items(items:Iterable[SimilarImage]):
            grouped = []
            for item in items:
                found_group = False
                for group in grouped:
                    if all(abs(item.image_hash - other.image_hash) < threshold for other in group):
                        group.append(item)
                        found_group = True
                        break
                if not found_group:
                    grouped.append([item])
            return grouped

        with ThreadPoolExecutor() as executor:
            hash_results = executor.map(process_hash, all_files)
            images_with_hashes = set(result for result in hash_results if result)

            grouped_items = [x for x in group_items(images_with_hashes) if len(x) > 1]
            for i in grouped_items:
                print(i)

        #     for x, y in itertools.product(images_with_hashes, images_with_hashes):
        #         if x and y:
        #             similarity = x.image_hash - y.image_hash
        #             if similarity < threshold:
        #                 if x is y:
        #                     continue
        #                 if y in similar_images:
        #                     if x in similar_images[y][similarity]:
        #                         continue
        #                 if x in similar_images:
        #                     if similarity in similar_images[x]:
        #                         similar_images[x][similarity].append(y)
        #                     else:
        #                         similar_images[x][similarity] = [y]
        #                 else:
        #                     similar_images[x] = {similarity: [y]}

        # return similar_images


@lru_cache(maxsize=20)
def get_supported_image(image_path, max_size: tuple[int, int] | None = (400, 400), as_b64: bool = False):
    with Image.open(image_path) as img:
        # Resize the image while maintaining the aspect ratio
        if max_size is not None:
            img.thumbnail(max_size)

        img_format = 'PNG'  # You can choose any supported format here

        if as_b64:
            buffered = BytesIO()
            img.save(buffered, format=img_format)
            img_base64 = base64.b64encode(buffered.getvalue())  # type: ignore
            return img_base64

        temp_folder = tempfile.gettempdir()
        temp_file = Path(temp_folder) / \
            f"{Path(image_path).stem}_{img_format.lower()}"
        img.save(f"{temp_file}.{img_format.lower()}", format=img_format)
        return str(temp_file) + f".{img_format.lower()}"
