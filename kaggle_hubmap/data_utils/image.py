import cv2
import logging
import os
import typing as t
from pathlib import Path

logger = logging.getLogger(__name__)


def get_image_meta(img_path: os.PathLike) -> t.Dict[str, t.Any]:
    """
    Returns dictionary of image metadata.
    
    Args:
        img_path: path to image file.
        
    Returns:
        Dictionary of image metadata.
    """
    img_path = Path(img_path)
    img = cv2.imread(str(img_path))
    img_meta = {
        'img_id': img_path.stem,
        'img_name': img_path.name,
        'img_ext': img_path.suffix,
        'img_dir': img_path.parent,
        'img_shape': img.shape,
        'img_size': os.path.getsize(img_path),
        'img_mean': img.mean(),
        'img_std': img.std(),
        'dtype': str(img.dtype)
    }
    
    return img_meta