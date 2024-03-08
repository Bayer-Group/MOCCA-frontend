from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True,init=True)
class CachedFile:
    """Information about cached file"""

    id: int
    """Unique ID of the cached file"""

    original_name: str
    """Original name of the uploaded file"""

    cached_path: str
    """Full path to the file in the cache directory"""
    

@dataclass(init=True, slots=True)
class CampaignProcessingInfo:
    """Status of the campaign processing running in background"""
    status : Literal['IDLE', 'PROCESSING', 'NEW_DATA_READY']
    message : str
    message_class : str