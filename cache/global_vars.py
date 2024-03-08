"""Functions for getting and setting global variables"""

from typing import Any, Dict

from mocca2 import MoccaDataset

from app import server, flask_cache
import cache

def _set(name : str, value : Any):
    """Sets variable value, not to be used outside this package"""
    with server.app_context():
        flask_cache.set(name, value)

def _get(name : str) -> Any:
    """Gets variable value, not to be used outside this package"""
    with server.app_context():
        value = flask_cache.get(name)
    
    return value

def init():
    """Initialize global variables"""
    set_campaign(MoccaDataset())
    set_cached_files(dict())
    set_current_blank(None)
    set_campaign_processing_info(
        cache.CampaignProcessingInfo("IDLE", "", ""))
    set_displayed_chromatogram(None)

# CAMPAIGN

def get_campaign() -> MoccaDataset:
    """Returns the current MOCCA campaign"""
    return _get('campaign')

def set_campaign(campaign: MoccaDataset):
    """Updates the current MOCCA campaign"""
    _set('campaign', campaign)

# CACHED FILES

def get_cached_files() -> Dict[int,cache.CachedFile]:
    """Returns dictionary with information about all cached files"""
    return _get('cached_files_info')

def set_cached_files(cached_files: Dict[int,cache.CachedFile]):
    """Sets the dictionary with information about all cached files"""
    _set('cached_files_info', cached_files)

# DATA PAGE - CURRENT BLANK

def get_current_blank() -> int | None:
    """Returns the cached file ID of the current blank file for uploading samples"""
    return _get('current_blank')

def set_current_blank(id: int | None):
    """Sets the cached file ID of the current blank file for uploading samples"""
    _set('current_blank', id)

# PROCESS PAGE - CAMPAIGN PROCESSING INFO

def get_campaign_processing_info() -> cache.CampaignProcessingInfo:
    """Returns the campaign processing status info"""
    return _get('campaign_processing_info')

def set_campaign_processing_info(status : cache.CampaignProcessingInfo):
    """Sets the campaign processing status info"""
    _set('campaign_processing_info', status)

# RESULTS PAGE - ID OF DISPLAYED CHROMATOGRAM

def get_displayed_chromatogram() -> int:
    """Returns the ID of the chromatogram shown on results page"""
    return _get('displayed_chromatogram_id')

def set_displayed_chromatogram(chromatogram_id: int):
    """Sets the ID of the chromatogram shown on results page"""
    _set('displayed_chromatogram_id', chromatogram_id)
