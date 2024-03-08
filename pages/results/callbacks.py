from dash import callback, Input, Output # type: ignore

from pages.results.layout_chromatogram import layout as layout_chromatogram
from pages.results.layout_table_concs import layout_area_perc, layout_conc, layout_conc_istd
from pages.results.layout_compounds import layout as layout_compounds

import cache

@callback(
    Output('results-div-tabs-content', 'children'),
    Input('results-tabs', 'value'),
)
def render_content(tab):
    """When tab is selected, renders the relevant content"""

    if len(cache.get_campaign().chromatograms) == 0:
        return "There aren't any chromatograms in the current campaign"

    if tab == 'chromatograms':
        return layout_chromatogram()
    elif tab == 'area_perc':
        return layout_area_perc()
    elif tab == 'conc':
        return layout_conc()
    elif tab == 'conc_istd':
        return layout_conc_istd()
    elif tab == 'compounds':
        return layout_compounds()
    else:
        return 'This tab is not implemented!'
