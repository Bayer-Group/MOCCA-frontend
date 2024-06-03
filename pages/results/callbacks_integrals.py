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


### CONCENTRATIONS - ABSOLUTE

def get_integrals_dataframe() -> pd.DataFrame:
    """Returns the absolute concentration data to be displayed"""

    current_campaign = cache.get_campaign()

    # Calculate the absolute concentrations
    df, _ = current_campaign.get_integrals()

    return df

### CONCENTRATIONS - ISTD

def get_rel_integrals_dataframe() -> pd.DataFrame:
    """Returns the concentrations relative to ISTD to be displayed"""

    current_campaign = cache.get_campaign()

    # Calculate the absolute concentrations
    df, _ = current_campaign.get_relative_integrals()

    return df