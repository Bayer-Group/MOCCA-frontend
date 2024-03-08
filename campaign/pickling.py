"""Functions in this file handle pickling and unpickling of the campaign"""

import pickle

from mocca2 import MoccaDataset

import cache

def pickle_all() -> str:
    """Pickles current campaign and all relevant files. Returns path to the pickle file"""

    current_campaign = cache.get_campaign()

    # Pickle all the data
    _, path = cache.add_cached_file('campaign.pkl')
    with open(path, "wb") as f:
        pickle.dump(current_campaign, f)
    
    return path

def unpickle_all(pickle_id: int):
    """Unpickles current_campaign and all relevant files from specified file"""

    pickle_path = cache.get_cached_file(pickle_id).cached_path

    # Load the PickleData class
    with open(pickle_path, "rb") as f:
        restored_campaign : MoccaDataset = pickle.load(f)

    # Restore the campaign
    cache.set_campaign(restored_campaign)
    




