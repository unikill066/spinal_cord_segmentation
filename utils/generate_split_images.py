#!/usr/bin/env python3
"""
Developed by Nikhil Nageshwar Inturi

This module provides ImageSplitter for splitting PNG images into
equal-sized sub-images and saving them to an output directory.
"""

# imports
from pathlib import Path
import numpy as np, cv2, logging
from PIL import Image
# local imports
from utils.constants import setup_logging
Image.MAX_IMAGE_PIXELS = None


class ImageSplitter:
    """
    Splits all PNG images in a source directory into sub-images of specified width and height.
    """

    def __init__(self, source_dir: Path, output_dir: Path, sub_image_width: int, sub_image_height: int) -> None:
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.sub_w = sub_image_width
        self.sub_h = sub_image_height
        self.logger = logging.getLogger(self.__class__.__name__)
        self._setup_output_directory()

    def _setup_output_directory(self) -> None:
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Output directory ready: {self.output_dir}")
        except Exception as e:
            self.logger.error(f"Failed to create output directory {self.output_dir}: {e}")
            raise

    def split_all(self) -> None:
        """
        Iterate over all PNG files in source_dir and split them.
        """
        png_files = list(self.source_dir.glob("*.png"))
        if not png_files:
            self.logger.warning(f"No .png files found in {self.source_dir}")
            return

        for png_file in png_files:
            try:
                self.split_file(png_file)
            except Exception:
                self.logger.exception(f"Error splitting file: {png_file}")

    def split_file(self, png_path: Path) -> None:
        """
        Split a single PNG image into sub-images.

        Args:
            png_path: Path to the input .png file.
        """
        with Image.open(png_path) as pil_img:
            img = np.array(pil_img)
        self.logger.debug(f"Loaded {png_path.name} with shape {img.shape}")

        height, width = img.shape[:2]
        cols = (width + self.sub_w - 1) // self.sub_w
        rows = (height + self.sub_h - 1) // self.sub_h

        for row in range(rows):
            for col in range(cols):
                x0 = col * self.sub_w
                y0 = row * self.sub_h
                x1 = min(x0 + self.sub_w, width)
                y1 = min(y0 + self.sub_h, height)
                sub_img = img[y0:y1, x0:x1]

                output_name = f"{png_path.stem}_{row}_{col}.png"
                output_path = self.output_dir / output_name
                # success = cv2.imwrite(str(output_path), sub_img)
                sub_img_bgr = cv2.cvtColor(sub_img, cv2.COLOR_RGB2BGR)
                success = cv2.imwrite(str(output_path), sub_img_bgr)
                if success:
                    self.logger.info(f"Saved sub-image: {output_name}")
                else:
                    self.logger.error(f"Failed to save sub-image: {output_name}")


# testing
# from bin.constants import setup_logging
# from bin.generate_split_images import ImageSplitter
# setup_logging(logging.INFO)
# splitter = ImageSplitter(source_dir=Path("path/to/pngs"), output_dir=Path("path/to/splits"), sub_image_width=640, sub_image_height=640)
# splitter.split_all()
