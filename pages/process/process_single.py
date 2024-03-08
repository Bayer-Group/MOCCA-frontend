from typing import Any

from dash import dcc # type: ignore

from mocca2 import MoccaDataset
from mocca2.dataset import ProcessingSettings

import cache
from pages.process.layout_chrom_preview import visualize_chromatogram

def process_single(settings: ProcessingSettings, sample_idx: int | None) -> str | Any:
    """Processes single sample. Either returns error message (string), or html elements with visualized data."""

    if sample_idx is None:
        return "Please select which sample should be analysed!"
    sample_idx = int(sample_idx)
    
    # create test campaign
    test_campaign = MoccaDataset()
    current_campaign = cache.get_campaign()
    sample = current_campaign.chromatograms[sample_idx]
    test_campaign.chromatograms[0] = sample
    test_campaign._raw_2d_data[0] = current_campaign._raw_2d_data[sample_idx]

    # process the test campaign
    test_campaign.process_all(settings)

    # create the plots
    chromatogram_plot, chromatogram_config = visualize_chromatogram(test_campaign, 0)
    chromatogram_plot = dcc.Graph(figure=chromatogram_plot, config=chromatogram_config)

    return chromatogram_plot