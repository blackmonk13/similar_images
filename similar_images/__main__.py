import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple, Union
from similar_images.similar_image import SimilarImage
from similar_images.similarity_finder import SimilarityFinder


def find_similarities(
    directory: str,
    threshold: int,
    recursive: bool,
) -> Dict[str, List[Dict[str, Union[str, Dict[str, Union[str, Tuple[int, int]]]]]]]:
    """Find similar images in a given directory"""
    dir_path = Path(directory)
    if not dir_path.exists():
        raise ValueError(f"Directory does not exist: {dir_path}")
    finder = SimilarityFinder()
    similar_images_groups: Dict[str, List[SimilarImage]] = finder.find_in_path(
        str(dir_path),
        recursive,
        threshold,
    )

    # Convert SimilarImage objects to dictionaries
    similar_images_groups_serializable = {
        group: [image.to_dict() for image in images]
        for group, images in similar_images_groups.items()
    }

    return similar_images_groups_serializable


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find similar images in a directory.")
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        default=10,
        help="Similarity threshold (default: 10)",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        type=bool,
        default=False,
        help="Iterate recursively in path",
    )
    parser.add_argument(
        "path",
        type=str,
        help="Path to the directory with images",
    )
    args = parser.parse_args()

    try:
        similarities = find_similarities(
            args.path,
            args.threshold,
            args.recursive,
        )
        print(json.dumps(similarities, indent=4))
    except ValueError as e:
        print(f"Error: {e}")
