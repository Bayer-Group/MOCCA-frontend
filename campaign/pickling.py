"""
Functions for dumping and loading the campaign object into .mocca2 file.

The mocca2 file is compressed JSON file - this prevents injection attacks while minimizing the file size.
"""

import zlib, json, re

from mocca2 import MoccaDataset

import cache


def pickle_all() -> str:
    """
    Dumps the current campaign into a .mocca2 file.

    The .mocca2 file is json compressed with zlib.
    """

    # compress current campaign to bytes
    current_campaign = cache.get_campaign()
    campaign_json = json.dumps(
        current_campaign.to_dict(),
        separators=(",", ":"),  # remove whitespace
    )

    # reduce the number of decimal places for floats
    def mround(match):
        return "{:.7f}".format(float(match.group()))

    campaign_json = re.sub(re.compile(r"\d+\.\d{7,}"), mround, campaign_json)

    # compress the JSON string
    campaign_json = zlib.compress(campaign_json.encode("utf-8"), level=9)

    # Save the compressed JSON to a file
    _, path = cache.add_cached_file("campaign.mocca2")
    with open(path, "wb") as f:
        f.write(campaign_json)

    return path


def unpickle_all(pickle_id: int):
    """
    Loads the campaign from a .mocca2 file

    The .mocca2 file is json compressed with zlib.
    """

    pickle_path = cache.get_cached_file(pickle_id).cached_path

    # Load the compressed JSON
    with open(pickle_path, "rb") as f:
        campaign_json = f.read()

    # deflate
    campaign_json = zlib.decompress(campaign_json).decode("utf-8")

    # Load the campaign from the JSON
    campaign_dict = json.loads(campaign_json)
    restored_campaign = MoccaDataset.from_dict(campaign_dict)

    # Restore the campaign
    cache.set_campaign(restored_campaign)
