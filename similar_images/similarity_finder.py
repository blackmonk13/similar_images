"""Similarity Finder"""
import itertools
import mimetypes
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Iterable, List, Optional

import imagehash
from PIL import Image, UnidentifiedImageError

from .disjoint_set import DisjointSet
from .similar_image import SimilarImage


class SimilarityFinder:
    """Similarity Finder"""

    def calculate_hash(self, image_path: str) -> Optional[imagehash.ImageHash]:
        """Calculate hash of given image path"""
        try:
            with Image.open(image_path) as image:
                hash_value = imagehash.average_hash(image)
                return hash_value
        except UnidentifiedImageError:
            return None

    def is_image(self, path: str) -> bool:
        """Check if the given path is a valid image"""
        mime_type = mimetypes.guess_type(path)
        if mime_type[0] is not None and mime_type[0].startswith("image"):
            return True
        return False

    def list_path(self, root_path: str) -> Iterable[str]:
        """List all files in the given directory"""
        for file_name in os.listdir(root_path):
            file_path = os.path.join(root_path, file_name).replace("\\", "/")
            if self.is_image(path=file_path):
                yield file_path

    def walk_path(self, root_path: str) -> Iterable[str]:
        """Iterate over the directory"""
        for root_path, _, files in os.walk(root_path):
            for file_name in files:
                file_path = os.path.join(root_path, file_name).replace("\\", "/")
                if self.is_image(path=file_path):
                    yield file_path

    def find_in_path(
        self,
        folder_path: str,
        recursive: bool = False,
        threshold: int = 10,
    ) -> Dict[str, List[SimilarImage]]:
        """Finds similar images in folder_path"""
        if recursive:
            all_files = list(self.walk_path(folder_path))
        else:
            all_files = list(self.list_path(folder_path))
        return self.find_similar_images(filelist=all_files, threshold=threshold)

    def find_similar_images(
        self,
        filelist: List[str],
        threshold: int = 10,
    ) -> Dict[str, List[SimilarImage]]:
        """Find similar images"""
        images_with_hashes: set[SimilarImage] = set()

        disjoint_set = DisjointSet(filelist)

        def process_hash(file: str) -> Optional[SimilarImage]:
            hash_value = self.calculate_hash(file)
            if hash_value is not None:
                return SimilarImage(file, hash_value)
            return None

        def compute_hash_difference(img1: SimilarImage, img2: SimilarImage) -> int:
            return img1.image_hash - img2.image_hash

        with ThreadPoolExecutor() as executor:
            hash_results = executor.map(process_hash, filelist)
            images_with_hashes = set(result for result in hash_results if result)

        # Calculate hash differences for all combinations
        hash_differences = []
        for img1, img2 in itertools.combinations(images_with_hashes, 2):
            hash_differences.append(compute_hash_difference(img1, img2))

        for (img1, img2), hash_difference in zip(
            itertools.combinations(images_with_hashes, 2), hash_differences
        ):
            if hash_difference <= threshold:
                disjoint_set.union(img1.image_path, img2.image_path)

        # Group images by their root representative
        image_groups: Dict[str, List[SimilarImage]] = {}
        for image in images_with_hashes:
            root = disjoint_set.find(image.image_path)
            if root not in image_groups:
                image_groups[root] = []
            image_groups[root].append(image)

        # Filter out groups with only one image
        filtered_image_groups = {
            root: group for root, group in image_groups.items() if len(group) > 1
        }

        return filtered_image_groups
