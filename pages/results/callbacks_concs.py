from typing import Dict, Tuple, List, Any

from dash import callback, Input, Output, State # type: ignore
import pandas as pd # type: ignore
import numpy as np

import cache

### COMMON FUNCTIONS

def get_columns(df: pd.DataFrame, decimals: int = 1) -> List[Dict[str, Any]]:
    cols = []
    for col in df.columns:
        if col == 'Chromatogram ID':
            continue

        if col == 'Chromatogram':
            cols += [{'id': col, 'name': col}]
            continue

        if col == '#ignore':
            continue
        
        cols += [{
            'id': col,
            'name': col,
            'type': 'numeric',
            'format': {'specifier': f'0.{decimals}f'}
        }]


    return cols

### AREA PERCENT TABLE

@callback(
    output=[
        Output('results-table-area-percent', 'data'),
        Output('results-table-area-percent', 'columns'),
        Output('results-h5-area-percent-wavelength', 'children')
    ],
    inputs=Input('button-set-wavelength-for-area', 'n_clicks'),
    state=State('input-wavelength-for-area', 'value')
)
def update_area_percent_table(_, wavelength):
    """Calculates the area% at given wavelength and updates the table"""

    df, wl = get_area_perc_dataframe(float(wavelength))
    cols = get_columns(df, 1)
    rows = df.to_dict('records')

    return rows, cols, f"Area % at {wl:0.0f} nm"

def get_area_perc_dataframe(wavelength: float) -> Tuple[pd.DataFrame, float]:
    """Returns the area % data to be displayed and the actual wavelength"""

    current_campaign = cache.get_campaign()

    # Calculate the area percent data at given wavelength
    wl_idx, wl = current_campaign.closest_wavelength(wavelength) # type: ignore
    df, _ = current_campaign.get_area_percent(wl_idx)

    return df, wl

### CONCENTRATIONS - ABSOLUTE

def get_concs_abs_dataframe() -> pd.DataFrame:
    """Returns the absolute concentration data to be displayed"""

    current_campaign = cache.get_campaign()

    # Calculate the absolute concentrations
    df, _ = current_campaign.get_concentrations()

    return df

### CONCENTRATIONS - ISTD

def get_concs_istd_dataframe() -> pd.DataFrame:
    """Returns the concentrations relative to ISTD to be displayed"""

    current_campaign = cache.get_campaign()

    # Calculate the absolute concentrations
    df, _ = current_campaign.get_relative_concentrations()

    return df