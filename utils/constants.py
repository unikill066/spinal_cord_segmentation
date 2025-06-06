# imports
import logging
from pathlib import Path
from typing import Union



def setup_logging(level: Union[int, str] = logging.INFO) -> None:
    """
    Configure the root logger format and level.
    """
    logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", level=level)

# setup_logging - usage
# from constants import setup_logging
# setup_logging(logging.INFO)

SCALING_FACTOR = 0.2125
IMG_HEIGHT, IMG_WIDTH = 1024, 1024  # 640, 640
# CONFIG_DIR = Path('/Users/discovery/Downloads/xenium_testing_jit/ish_hDGR_samples_fr')
CONFIG_DIR = Path('/Users/discovery/Downloads/xenium_testing_jit/spinal_cord_samples_fr')

TIF_IMAGES_DIR = CONFIG_DIR / '1_tif_images'

PNG_IMAGES_DIR = CONFIG_DIR / '2_png_images'
SPLIT_IMAGES_DIR = CONFIG_DIR / '3_split_images'
CELLPOSE_MASKS_DIR = CONFIG_DIR / '4_cellpose_masks'
STITCHED_MASKS_DIR = CONFIG_DIR / '5_stitched_masks'
OUTPUT_DIR = CONFIG_DIR / '6_output_masks'

MASKS_DIR = 'masks'
PREVIEW_DIR = 'preview'
SEGMENTATION_DIR = 'segmentation'