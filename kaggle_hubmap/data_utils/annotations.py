import cv2
import json
import logging
import os
import shutil
import numpy as np
import pandas as pd
import typing as t
from ast import literal_eval
from pathlib import Path

logger = logging.getLogger(__name__)

LABEL_MAP = {'blood_vessel': 1, 'glomerulus': 2, 'unsure': 3}


def read_json_file(file_path: os.PathLike) -> t.List[t.Dict[str, t.Any]]:
    """
    Reads a JSON file and returns a list of dictionaries.
    """
    json_data = []
    with open(file_path, 'r') as file:
        for line in file:
            # Skip empty lines or lines containing only whitespace
            if line.strip():
                json_obj = json.loads(line)
                json_data.append(json_obj)
        
    return json_data

def copy_to_id_parent_dir(img_path: os.PathLike, dst_dir: os.PathLike) -> None:
    """
    Copies image file to a directory named after the image id.
    
    Args:
        img_path: path to image file.
        dst_dir: destination directory.
        
    Returns:
        None
    """
    id = Path(img_path).stem
    dst_path = Path(dst_dir) / id / 'img.tif'
    if not dst_path.parent.exists():
        dst_path.parent.mkdir(parents=True)
    
    shutil.copy2(img_path, dst_path)

def convert_point_annotations_to_mask_array(
    image_path: os.PathLike,
    annotations_df: pd.DataFrame
    ) -> None:
    """
    Converts point annotations to a mask array and saves it to disk
    in the same directory as the image file.
    
    Args:
        image_path: path to image file.
        annotations_df: dataframe containing annotations and image IDs.
        
    Returns:
        None
    """
    id = Path(image_path).parent.name
    if id not in annotations_df['id'].to_list():
        logger.warning(f'No annotations found for image {id}')
        
        return {'img_path': image_path, 'status': 'failed'}
    
    else:
        logger.info(f'Converting annotations to mask for image {id}')
        annotations_list = \
            literal_eval(
                annotations_df.query('id == @id')['annotations'].values.tolist()[0])
        mask_path = str(Path(image_path).parent / 'mask.tif')
        
        img = cv2.imread(image_path)
        mask = np.zeros(img.shape[:-1], dtype='uint8')
        
        for ann in annotations_list:
            pts = np.array(ann['coordinates'], dtype=np.int32)
            cv2.fillPoly(mask, [pts], LABEL_MAP[ann['type']])
            
        logger.info(f'Writing mask to {mask_path}')
        cv2.imwrite(mask_path, mask)
        
        return {'img_path': image_path, 'status': 'success'}
    
    