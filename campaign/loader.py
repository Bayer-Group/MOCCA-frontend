"""This file contains routines for restoring campaign from .pkl file"""

from typing import Dict, List, Tuple

import cache


def gen_upload_table_from_campaign() -> Tuple[List[Dict], str]:
    """Uses the data stored in `current_campaign` to generate the upload data table"""
    data = list()

    current_campaign = cache.get_campaign()

    istd = current_campaign.istd_compound
    if istd is not None:
        istd_name = current_campaign.compounds[istd].name
        if istd_name is None:
            istd_name = ""
    else:
        istd_name = ""

    for idx, chromatogram in current_campaign.chromatograms.items():
        compound_name = None
        compound_conc = None
        if idx in current_campaign.compound_references:
            compound_name, compound_conc = current_campaign.compound_references[idx]

        istd_conc = current_campaign.istd_concentrations[idx] \
            if idx in current_campaign.istd_concentrations else None

        # create the entry for table
        row = dict(
            chromatogram_id=idx,
            sample_id=None,
            blank_id=None,
            name=chromatogram.name,
            sample=chromatogram.sample_path,
            blank=chromatogram.blank_path,
            compound_name=compound_name,
            compound_conc=compound_conc,
            istd_conc=istd_conc
        )
        data.append(row)

    return data, istd_name
