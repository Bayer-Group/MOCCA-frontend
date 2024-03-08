"""This module has to be used for all global variables and cached files!!!"""

from cache.classes import CachedFile, CampaignProcessingInfo

from cache.global_vars import get_campaign, set_campaign
from cache.global_vars import get_cached_files, set_cached_files
from cache.global_vars import get_current_blank, set_current_blank
from cache.global_vars import get_campaign_processing_info, set_campaign_processing_info
from cache.global_vars import get_displayed_chromatogram, set_displayed_chromatogram

from cache.files import add_cached_file, get_cached_file

from cache.uploading_files import save_uploaded_file

from cache.global_vars import init as init_vars
from cache.files import init as init_files

def init():
    """Initialize cache"""
    init_vars()
    init_files()