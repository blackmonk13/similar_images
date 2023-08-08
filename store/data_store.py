import os
from pathlib import Path
from typing import Dict, List, OrderedDict
from send2trash import send2trash

from core.similar_image import SimilarImage


class DataStore:
    def __init__(self):
        self._similarities: OrderedDict[SimilarImage, OrderedDict[int, List[SimilarImage]]] = OrderedDict()

    @property
    def similarities(self):
        return self._similarities

    @similarities.setter
    def similarities(self, data: OrderedDict[SimilarImage, OrderedDict[int, List[SimilarImage]]]):
        self._similarities = data
        

    def remove_similarity(self, image: SimilarImage, delete: bool = False) -> None:
        """
        Remove a specific similarity from the list of similar images based on the given path.
        Optionally, delete the file from the file system.

        :param image: The image to remove.
        :param delete: A boolean flag indicating whether to delete the file from the file system.
        """
        # # Filter out the SimilarImage instances containing the specified path
        # self._similarities = [
        #     item for item in self._similarities if item.image_path is not path
        # ]
        del self._similarities[image]
        for item, similarities in self._similarities.items():
            for sim in similarities:
                self._similarities[item][sim].remove(image)
                if not self._similarities[item][sim]:
                    self._similarities[item][sim]
        

        # Delete the file if the 'delete' parameter is set to True
        path_to_delete = Path(image.image_path)
        if delete and path_to_delete.exists():
            send2trash(str(path_to_delete))