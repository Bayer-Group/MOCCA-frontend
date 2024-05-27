from typing import List, Dict, Tuple, Any

import warnings
from mocca2 import MoccaDataset, Chromatogram
import numpy as np

import cache


def campaign_from_table(data: List[Dict], istd: str | None = None) -> None:
    """
    Tries to create MOCCA campaign from the upload table (on `data` page).
    """

    old_campaign = cache.get_campaign()

    # Create campaign
    camp = MoccaDataset()

    # Copy settings from current campaign
    camp.settings = old_campaign.settings

    # get name of ISTD and check that it is in data
    if istd == "":
        istd = None
    if istd is not None:
        if istd not in [d["compound_name"] for d in data]:
            raise Exception("Cannot find reference chromatogram for internal standard!")

    def parse_data(
        row: Dict[str, Any]
    ) -> Tuple[str | None, float | None, float | None]:
        # Check whether the compound and it's concentrations are known
        compound_name = row["compound_name"]
        if compound_name == "":
            compound_name = None

        compound_conc = None
        if row["compound_conc"] != "" and row["compound_conc"] is not None:
            try:
                compound_conc = float(row["compound_conc"])
            except:
                raise Exception("Cannot convert Compound Concentration to a number!")

        # Get concentration of internal standard
        istd_conc = None
        if row["istd_conc"] != "" and row["istd_conc"] is not None:
            try:
                istd_conc = float(row["istd_conc"])
            except:
                raise Exception("Cannot convert ISTD Concentration to a number!")

        # Some sanity checks on table entries
        if compound_name is None and compound_conc is not None:
            raise Exception(
                "Please specify Compound Name if you specify Concentration!"
            )

        return compound_name, compound_conc, istd_conc

    # Copy chromatograms that are already loaded
    for row in data:
        idx = row["chromatogram_id"]
        if idx is not None:
            camp.chromatograms[idx] = old_campaign.chromatograms[idx]
            camp._raw_2d_data[idx] = old_campaign._raw_2d_data[idx]
            # update data from the table
            compound_name, compound_conc, istd_conc = parse_data(row)
            if compound_name is not None:
                camp.compound_references[idx] = (compound_name, compound_conc)
            if istd_conc is not None:
                camp.istd_concentrations[idx] = istd_conc
            camp.chromatograms[idx].name = row["name"]
            if istd is not None and row["compound_name"] == istd:
                camp._istd_chromatogram = row["chromatogram_id"]

    # Add the samples to the campaign
    for row in data:
        if row["chromatogram_id"] is not None:
            continue

        # Get the paths to the cached files
        cached_sample = cache.get_cached_file(int(row["sample_id"]))

        if row["blank_id"] == "" or row["blank_id"] is None:
            cached_blank = None
        else:
            cached_blank = cache.get_cached_file(int(row["blank_id"]))

        # Get compound names and concentrations
        compound_name, compound_conc, istd_conc = parse_data(row)

        # Add all the data to to campaign
        chromatogram = Chromatogram(
            sample=cached_sample.cached_path,
            blank=cached_blank.cached_path if cached_blank is not None else None,
            name=row["name"],
            interpolate_blank=True,
        )

        istd_reference = istd is not None and istd == compound_name

        # check that the chromatogram has the same sampling as the other ones
        if len(camp.chromatograms) > 0:
            if chromatogram.time.shape != camp.chromatograms[
                0
            ].time.shape or not np.allclose(
                chromatogram.time, camp.chromatograms[0].time
            ):
                warnings.warn("Chromatograms have different sampling rates!")
                chromatogram.interpolate_time(camp.chromatograms[0].time, inplace=True)

        # add chromatogram to campaign
        idx = camp.add_chromatogram(
            chromatogram=chromatogram,
            istd_concentration=istd_conc,
            reference_for_compound=compound_name,
            compound_concentration=compound_conc,
            istd_reference=istd_reference,
        )

        # Change chromatogram paths to the original paths
        # Once the chromatogram data is loaded, the paths are there only for info
        camp.chromatograms[idx].sample_path = cached_sample.original_name
        if cached_blank is not None:
            camp.chromatograms[idx].blank_path = cached_blank.original_name
        camp.chromatograms[idx].name = row["name"]

    # Store the new campaign in the global variable
    cache.set_campaign(camp)
