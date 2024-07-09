"""Entry point for the CLI."""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Union

from similar_images.similar_image import SimilarImage
from similar_images.similarity_finder import SimilarityFinder


def find_similarities(
    directory: str,
    threshold: int,
    recursive: bool,
) -> Dict[str, List[Dict[str, Union[str, Dict[str, Union[str, Tuple[int, int]]]]]]]:
    """Find similar images in a given directory.

    Args:
        directory (str): Path to the directory containing images.
        threshold (int): Similarity threshold.
        recursive (bool): Flag to enable/disable recursive directory scanning.
        output_format (str): Desired output format (json or csv).
        output_file (str): Path to the output file.

    Returns:
        dict: A dictionary containing groups of similar images.
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        raise FileNotFoundError(f"Directory does not exist: {dir_path}")
    if not dir_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {dir_path}")
    if not os.access(dir_path, os.R_OK):
        raise PermissionError(f"Permission denied: {dir_path}")

    finder = SimilarityFinder()

    if recursive:
        all_files = list(finder.walk_path(directory))
    else:
        all_files = list(finder.list_path(directory))

    # total_images = len(all_files)
    # sys.stderr.write(f"Processing {total_images} images...\n")

    similar_images_groups: Dict[str, List[SimilarImage]] = finder.find_similar_images(
        filelist=all_files,
        threshold=threshold,
    )

    # Convert SimilarImage objects to dictionaries
    similar_images_groups_serializable = {
        group: [image.to_dict() for image in images]
        for group, images in similar_images_groups.items()
    }

    return similar_images_groups_serializable


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        prog="similar_images", description="Find similar images in a directory."
    )
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
        action="store_true",
        help="Iterate recursively in path",
    )
    parser.add_argument(
        "-o",
        "--output-format",
        type=str,
        default="json",
        choices=["json", "csv"],
        help="Output format (default: json)",
    )
    parser.add_argument(
        "-f",
        "--output-file",
        type=str,
        default="",
        help="Path to the output file",
    )
    parser.add_argument(
        "path",
        type=str,
        help="Path to the directory with images",
    )
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0.1")

    args = parser.parse_args()

    try:
        output_format = args.output_format
        output_file = args.output_file
        results = find_similarities(
            args.path,
            args.threshold,
            args.recursive,
        )

        if output_format == "json":
            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(results, f, indent=4)
            else:
                print(json.dumps(results, indent=4))
        elif output_format == "csv":
            # Implement CSV output here
            raise NotImplementedError("CSV output is not yet implemented")
        else:
            raise ValueError("Invalid output format")

        # similar_image_groups_count = len(results)
        # sys.stderr.write(
        #     f"Found {similar_image_groups_count} groups of similar images.\n"
        # )
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
