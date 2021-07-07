import os

from typing import Callable, List
from ruia.utils import get_logger

__all__ = ['get_file_paths']

logger = get_logger('Ocr')


def get_file_paths(dir, filter_files: Callable[[str], bool] = None, num=None, *, key=None, base_name=False) -> List[str]:
    res = []
    for root, dirs, files in os.walk(dir):
        if filter_files:
            for file in files:
                if filter_files(file):
                    res.append(os.path.abspath(os.path.join(root, file)))
        else:
            for file in files:
                res.append(os.path.abspath(os.path.join(root, file)))
    return_value = res[:num] if num else res
    if base_name:
        return_value = [os.path.basename(v) for v in return_value]
    if key:
        return_value.sort(key=key)
    return return_value
