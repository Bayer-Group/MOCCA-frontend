from typing import Dict

from dash import callback, Input, Output, Patch # type: ignore
from plotly import graph_objects as go # type: ignore
import numpy as np

import cache

@callback(
    Output('results-graph-compound-absorption', 'figure', allow_duplicate=True),
    Input("results-dropdown-compound-spectrum", "value"),
    prevent_initial_call='initial_duplicate'
)
def change_compound_callback(compound):
    """Changes the shown absorption spectrum of a compound on the results page"""
    if compound is None:
        return Patch()
    
    fig = create_figure(int(compound))

    return fig

@callback(
    Output("results-dropdown-compound-spectrum", "options"),
    Input("results-table-compounds", "data"),
    prevent_initial_call='initial_duplicate'
)
def rename_compounds(data):
    """Changes the names of the compounds"""
    
    current_campaign = cache.get_campaign()

    for row in data:
        current_campaign.compounds[int(row['ID'])].name = row['Compound']
    
    cache.set_campaign(current_campaign)

    return {idx: comp.name for idx, comp in current_campaign.compounds.items()}

def create_figure(compound: int) -> Dict:
    """Creates the figure showing absorption spectrum of given compound"""
    current_campaign = cache.get_campaign()

    wl = np.array(current_campaign.wavelength())
    absorbance = current_campaign.compounds[compound].spectrum

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=wl, y=absorbance, mode='lines', name=f'Absorbance', line={'color':'black'}))

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='rgb(0,0,0)',
            linewidth=1,
            ticks='outside',
            tickfont_size=13
        ),
        yaxis=dict(
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='rgb(0,0,0)',
            linewidth=1,
            ticks='outside'
        ),
        showlegend=False,
        plot_bgcolor='white',
        font={'color': 'black', 'size': 15},
        xaxis_title="Wavelength [nm]",
        yaxis_title="Absorbance",
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode = 'x unified'
    )


    return fig.to_dict()