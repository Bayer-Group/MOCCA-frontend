"""This file contains functions for plotting chromatogram preview"""

from typing import Literal, Dict, Tuple

import plotly.graph_objects as go # type: ignore
from plotly.graph_objects import Figure
import numpy as np

from mocca2 import MoccaDataset


def visualize_chromatogram(current_campaign: MoccaDataset, chromatogram_id: int) -> Tuple[Figure, Dict]:
    """Creates a plotly figure with absorbace over time and highlighted peaks. Returns plotly figure and config"""

    data = current_campaign.chromatograms[chromatogram_id].data

    time = current_campaign.time()
    assert time is not None

    fig = go.Figure()

    averaged_abs = np.mean(data, axis=0)
    fig.add_trace(go.Scatter(
        x=time,
        y=averaged_abs,
        mode='lines',
        name=f'Average',
        line={'width':1., 'color':'black'},
        hoverinfo='none'
    ))

    y_label = f"Abs. [mAU]"

    for peak in current_campaign.chromatograms[chromatogram_id].peaks:
        if peak.resolved and len(peak.components) < 2:
            color = '#00bf10'
        elif peak.resolved:
            color = '#ffbb00'
        else:
            color = '#bf0000'

        fig.add_vrect(
            x0=time[peak.left],
            x1=time[peak.right],
            fillcolor=color,
            opacity=0.1,
            line_width=1,
        )

        peak_time = peak.time(time)
        for idx, component in enumerate(peak.components):
            fig.add_trace(go.Scatter(
                x=peak_time,
                y=component.concentration,
                mode='lines',
                name=f'Component {idx+1}',
                line={'width':1.},
                fill='tozeroy',
                opacity=0.2,
                hoverinfo='none'
            ))

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
        xaxis_title="Time [min]",
        yaxis_title=y_label,
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode='x unified'
    )

    config = {
        'displayModeBar': False
    }

    return fig, config
