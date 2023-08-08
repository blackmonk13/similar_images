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
from typing import Dict, Iterable, List, OrderedDict, Tuple
from functools import lru_cache

from core.similar_image import SimilarImage


class SimilarityFinder:
    def calculate_hash(self, image_path: str) -> imagehash.ImageHash | None:
        try:
            with Image.open(image_path) as image:
                hash_value = imagehash.average_hash(image)
                return hash_value
        except UnidentifiedImageError:
            return None

    def is_image(self, path: str) -> bool:
        mime_type = mimetypes.guess_type(path)
        if mime_type[0] is not None and mime_type[0].startswith("image"):
            return True
        return False

    def list_path(self, root_path: str) -> Iterable[str]:
        for file_name in os.listdir(root_path):
            file_path = os.path.join(
                root_path, file_name).replace("\\", "/")
            if self.is_image(path=file_path):
                yield file_path

    def walk_path(self, root_path: str) -> Iterable[str]:
        for root_path, directories, files in os.walk(root_path):
            for file_name in files:
                file_path = os.path.join(
                    root_path, file_name).replace("\\", "/")
                if self.is_image(path=file_path):
                    yield file_path

    def find_similar_images(self, folder_path: str, threshold: int = 10):
        images_with_hashes: set[SimilarImage] = set()
        all_files = self.walk_path(folder_path)
        similar_images: OrderedDict[SimilarImage, OrderedDict[int, List[SimilarImage]]] = OrderedDict()

        def process_hash(file: str):
            hash_value = self.calculate_hash(file)
            if hash_value is not None:
                return SimilarImage(file, hash_value)

        def images_exist(images: List[SimilarImage], difference: int):
            exists = False
            for sim in similar_images.values():
                try:
                    if sim[difference] and any(img in sim[difference] for img in images):
                        exists = True
                        break
                except KeyError:
                    continue
            return exists

        with ThreadPoolExecutor() as executor:
            hash_results = executor.map(process_hash, all_files)
            images_with_hashes = set(
                result for result in hash_results if result)

        for img1, img2 in itertools.combinations(images_with_hashes, 2):
            hash_difference = img1.image_hash - img2.image_hash
            if hash_difference <= threshold:
                if images_exist([img1, img2], hash_difference):
                    continue
                if img1 not in similar_images:
                    similar_images[img1] = OrderedDict()
                if hash_difference not in similar_images[img1]:
                    similar_images[img1][hash_difference] = []
                similar_images[img1][hash_difference].append(img2)

        return similar_images


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
