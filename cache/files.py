from typing import Tuple

import os

from app import CACHE_DIR
import cache

def init():
    """Initializes file caching"""

    # create cache directory if doesn't exist
    if not os.path.exists(CACHE_DIR):
        os.mkdir(CACHE_DIR)

def get_cached_file(id: int) -> cache.CachedFile:
    """Returns the CachedFile with given ID"""
    files = cache.get_cached_files()

    return files[id]

def add_cached_file(original_name : str) -> Tuple[int, str]:
    """Returns ID and full path for location where new cached file can be saved"""
    id = _find_new_id()
    filename = _get_filename(id)
    extension = original_name.split('.')[-1]
    cached_path = os.path.join(CACHE_DIR, filename + '.' + extension)

    files = cache.get_cached_files()
    files[id] = cache.CachedFile(id, original_name, cached_path)
    cache.set_cached_files(files)

    return id, cached_path

def _get_filename(id: int) -> str:
    """Generates filename for caching from ID"""
    return f"cached{id:04.0f}"

def _find_new_id() -> int:
    """Finds lowest ID for cached file that is not currently used"""

    files = cache.get_cached_files()

    # assuming that less than 10 000 files will be cached
    for id in range(10000):
        if id not in files:
            return id
    
    raise Exception("Could not find suitable ID for cache file - maybe delete old files from cache folder?")