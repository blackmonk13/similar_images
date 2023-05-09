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
from typing import List, Tuple
from functools import lru_cache


class ImageSimilarityFinder:
    def walk_path(self, root_path: str) -> List[str]:
        file_paths: List[str] = []
        for root_path, directories, files in os.walk(root_path):
            for file_name in files:
                file_path = os.path.join(
                    root_path, file_name).replace("\\", "/")
                mime_type = mimetypes.guess_type(file_path)
                if mime_type[0] is not None and mime_type[0].startswith("image"):
                    file_paths.append(file_path)
        return file_paths

    def find_similar_images(self, folder_dir: str, threshold: int = 10) -> List[Tuple[str, str, int]]:
        image_hashes = {}
        all_files = self.walk_path(folder_dir)

        with ThreadPoolExecutor() as executor:
            results = executor.map(process_image_similarity, all_files)
            for file, result in zip(all_files, results):
                if result is not None:
                    image_hashes[file] = result

        similar_images = []
        for file1, hash1 in image_hashes.items():
            for file2, hash2 in image_hashes.items():
                if file1 != file2 and hash1 - hash2 < threshold:
                    if not similar_images.__contains__((file2, file1, hash2-hash1)):
                        similar_images.append((file1, file2, hash1-hash2))

        return similar_images

@lru_cache(maxsize=20)
def process_image_similarity(image_path: str) -> imagehash.ImageHash | None:
        try:
            with Image.open(image_path) as image:
                hash_value = imagehash.average_hash(image)
                return hash_value
        except UnidentifiedImageError:
            return None

@lru_cache(maxsize=20)
def get_aspect_ratio(width: int, height: int) -> tuple[int, int]:
    divisor = gcd(width, height) # type: ignore
    return width // divisor, height // divisor

@lru_cache(maxsize=20)
def get_size_auto(file_path: str):
    file_size = os.path.getsize(file_path)
    units = ['bytes', 'kb', 'mb', 'gb', 'tb']
    exponents_map = {unit: i for i, unit in enumerate(units)}

    for unit in units[::-1]:
        size = file_size / (1024 ** exponents_map[unit])
        if size >= 1:
            return round(size, 3), unit
    return 0, units[0]


@lru_cache(maxsize=20)
def get_image_info(image_path: str):
    with Image.open(image_path) as img:
        width, height = img.size
        aspect_ratio = get_aspect_ratio(width, height)

        # reader = imageio.get_reader(image_path, format='.tif')
        # metadata = reader.get_meta_data()
        # pixel_density = 1.0 / metadata["resolution"][0]
        bit_depth = img.mode
        size, unit = get_size_auto(image_path)
        return {
            "dimensions": (width, height),
            "size": f"{size} {unit}",
            # "pixel_density": pixel_density,
            "bit_depth": bit_depth,
            "aspect_ratio": f"{aspect_ratio[0]} / {aspect_ratio[1]}",
            "path": image_path,
        }


@lru_cache(maxsize=20)
def get_supported_image(image_path, max_size: tuple[int, int] | None = (400, 400), as_b64: bool = False):
    with Image.open(image_path) as img:
        # Resize the image while maintaining the aspect ratio
        if max_size is not None:
            img.thumbnail(max_size)

        # Resize the image while maintaining the aspect ratio
        if max_size is not None:
            img.thumbnail(max_size)

        img_format = 'PNG'  # You can choose any supported format here

        if as_b64:
            buffered = BytesIO()
            img.save(buffered, format=img_format)
            img_base64 = base64.b64encode(buffered.getvalue())
            return img_base64

        temp_folder = tempfile.gettempdir()
        temp_file = Path(temp_folder) / \
            f"{Path(image_path).stem}_{img_format.lower()}"
        img.save(f"{temp_file}.{img_format.lower()}", format=img_format)
        return str(temp_file) + f".{img_format.lower()}"


def walk_path(parent_path: str) -> list[str]:
    file_paths: list[str] = []
    for parent_path, directories, files in os.walk(parent_path):
        print(f"Checking: {parent_path}")
        for file_name in files:
            file_path = os.path.join(parent_path, file_name).replace("\\", "/")
            file_paths.append(file_path)
    return file_paths
