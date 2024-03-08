"""This file contains functions for creating 2D DAD chromatogram view, and associated callbacks"""

from typing import List, Dict

from dash import dcc, html, Input, Output, callback, Patch  # type: ignore
import numpy as np
from plotly import graph_objects as go  # type: ignore
from plotly.subplots import make_subplots  # type: ignore
from plotly.express.colors import hex_to_rgb, qualitative as plotly_colors # type: ignore

from mocca2.classes import Peak, DeconvolvedPeak, Compound
from mocca2 import MoccaDataset

import cache

# Indeces of the subplots, this is solely for readability
subplots = dict(
    # these are in fig['data']
    heatmap=0,
    chromatogram=1,
    spectrum=2,
    # these are in fig['layout']['shapes']
    hline_heatmap=0,
    hline_spectrum=1,
    vline_heatmap=2,
    vline_chromatogram=3
)


def create_figure(only_figure: bool = True) -> html.Div:
    """Creates interactive plotly figure that shows DAD data. Returns a Dash html.Div element"""

    current_campaign = cache.get_campaign()
    chromatogram_id = cache.get_displayed_chromatogram()

    time = current_campaign.time()
    wavelength = current_campaign.wavelength()
    assert time is not None and wavelength is not None
    data = current_campaign.chromatograms[chromatogram_id].data
    peaks = current_campaign.chromatograms[chromatogram_id].peaks

    # Find highest peak for initializing corss-section
    max_wl_idx, max_t_idx = np.unravel_index(np.argmax(data), data.shape)
    max_wl = wavelength[max_wl_idx]
    max_t = time[max_t_idx]

    # Initialize figure
    fig = make_subplots(
        rows=2,
        cols=2,
        shared_xaxes=True,
        shared_yaxes=True,
        horizontal_spacing=0.01,
        vertical_spacing=0.01,
        column_widths=[0.7, 0.3],
    )

    # Create subplots
    heatmap = go.Heatmap(
        x=time,
        y=wavelength,
        z=data,
        hoverinfo='none',
        colorscale='Rainbow',
        showscale=False
    )
    fig.add_trace(heatmap, col=1, row=1)

    chromatogram = go.Scatter(
        x=time,
        y=data[max_wl_idx],
        mode="lines",
        line={'color': 'black', 'width': 1.},
        hoverinfo='none'
    )
    fig.add_trace(chromatogram, col=1, row=2)

    spectrum = go.Scatter(
        x=data[:, max_t_idx],
        y=wavelength,
        mode="lines",
        line={'color': 'red', 'width': 1.},
        hoverinfo='none'
    )
    fig.add_trace(spectrum, col=2, row=1)

    # Add cross-section lines
    line_style = dict(line_dash="dash", line_width=1, opacity=1)

    fig.add_hline(row=1, col=1, y=max_wl, line_color="white", **line_style)
    fig.add_hline(row=1, col=2, y=max_wl, line_color="black", **line_style)
    fig.add_vline(row=1, col=1, x=max_t, line_color="white", **line_style)
    fig.add_vline(row=2, col=1, x=max_t, line_color="red", **line_style)

    # Add peak annotations
    fig = add_peak_annotations(fig, peaks, current_campaign.compounds)

    # Add component traces
    create_component_traces(fig, current_campaign, max_wl_idx, current_campaign.compounds)

    # General layout settings
    fig.update_layout(
        plot_bgcolor='#f0f0f0',
        margin=dict(l=0, r=0, b=0, t=0),
        showlegend=False,
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    # Set axis limits
    fig.update_xaxes(col=1, range=[time[0], time[-1]])
    fig.update_yaxes(row=1, range=[wavelength[0], wavelength[-1]][::-1])
    fig.update_xaxes(col=2, autorange="reversed")
    fig.update_yaxes(row=2, autorange=True)

    # On hover, have perpendicular lines across all three subplots
    # fig.data[0].update(xaxis="x3", yaxis="y2")
    # fig.update_xaxes(showspikes=True, spikemode="across",
    #                  spikecolor='#808080', spikesnap="cursor", spikethickness=0.5, col=1)
    # fig.update_yaxes(showspikes=True, spikemode="across",
    #                  spikecolor='#808080', spikesnap="cursor", spikethickness=0.5, row=1)

    # Configure ticks location and labels
    fig.update_xaxes(row=1, col=1, tickmode='array', tickvals=[])
    fig.update_yaxes(row=1, col=1, tickmode='array', tickvals=[])

    fig.update_xaxes(row=2, col=1,
                     title="Time [min]", side="bottom", showticklabels=True)
    fig.update_yaxes(row=2, col=1,
                     title="Absorbance [mAU]", side="right", showticklabels=True)

    fig.update_xaxes(row=1, col=2,
                     title="Absorbance [mAU]", side="bottom",  showticklabels=True)
    fig.update_yaxes(row=1, col=2,
                     title="Wavelength [nm]", side="right", showticklabels=True)


    if only_figure:
        return fig
    
    # Create html.Div element
    chromatogram_div = html.Div([
        html.Div(
            children=[
                html.Label("Contrast:"),
                dcc.Slider(
                    np.min(data), np.max(data),
                    marks=None,
                    value=np.max(data),
                    id='slider-chromatogram-limits',
                    className="py-0 pr-0 pl-2"
                )
            ],
            style={
                'display': 'grid',
                'grid-template-columns': 'auto 1fr',
                'align-items': 'center',
                'column-gap': '2ch',
            }
        ),
        dcc.Graph(
            figure=fig,
            style={'height': '100%', 'width': '100%'},
            id="results-figure-chromatogram",
            config={'displayModeBar': False}
        ),

    ],
        style={'height': '70vh', 'width': '100%'}
    )

    return chromatogram_div


def update_wl(fig, wl_idx, current_campaign: MoccaDataset):
    """Updates the position of the cross-section line on the wavelenght axis"""
    chr_id = cache.get_displayed_chromatogram()

    data = current_campaign.chromatograms[chr_id].data
    wavelength = current_campaign.wavelength()
    assert wavelength is not None

    fig['data'][subplots['chromatogram']]['y'] = data[wl_idx]
    fig['layout']['shapes'][subplots['hline_heatmap']]['y0'] = wavelength[wl_idx]
    fig['layout']['shapes'][subplots['hline_heatmap']]['y1'] = wavelength[wl_idx]
    fig['layout']['shapes'][subplots['hline_spectrum']]['y0'] = wavelength[wl_idx]
    fig['layout']['shapes'][subplots['hline_spectrum']]['y1'] = wavelength[wl_idx]

    peaks = current_campaign.chromatograms[chr_id].peaks
    time = current_campaign.time()
    assert time is not None

    trace_idx = 2
    for peak in peaks:
        for component in peak.components:
            compound = current_campaign.compounds[component.compound_id]
            if compound.name == '#ignore':
                continue
            trace_idx += 1
            fig['data'][trace_idx]['y'] = component.concentration * compound.spectrum[wl_idx]

    return fig


def update_time(fig, t_idx, current_campaign: MoccaDataset):
    """Updates the position of the cross-section line on the wavelenght axis"""
    chr_id = cache.get_displayed_chromatogram()

    data = current_campaign.chromatograms[chr_id].data
    time = current_campaign.time()
    assert time is not None

    fig['data'][subplots['spectrum']]['x'] = data[:, t_idx]
    fig['layout']['shapes'][subplots['vline_heatmap']]['x0'] = time[t_idx]
    fig['layout']['shapes'][subplots['vline_heatmap']]['x1'] = time[t_idx]
    fig['layout']['shapes'][subplots['vline_chromatogram']]['x0'] = time[t_idx]
    fig['layout']['shapes'][subplots['vline_chromatogram']]['x1'] = time[t_idx]

    return fig

def add_peak_annotations(fig: go.Figure, peaks: List[Peak | DeconvolvedPeak], compounds: Dict[int, Compound], shapes: bool = True) -> go.Figure:
    """Adds rectangles and peaks names to the chromatogram subplot"""
    current_campaign = cache.get_campaign()

    time = current_campaign.time()
    assert time is not None

    for peak in peaks:
        if peak.resolved and len(peak.components) < 2:
            color = '#00bf10'
        elif peak.resolved:
            color = '#ffbb00'
        else:
            color = '#bf0000'

        peak_name = '<br>'.join([(
            compounds[comp.compound_id].name  # type: ignore
            if comp.compound_id is not None and compounds[comp.compound_id].name is not None else "(?)"
        )
            for comp in sorted(peak.components, key=lambda f: -f.elution_time)
            if compounds[comp.compound_id].name != '#ignore'
        ])
        
        if len(peak_name) == 0:
            continue

        vrect = dict(
            type='rect',
            xref='x3',
            x0=time[peak.left],
            x1=time[peak.right],
            yref='y3 domain',
            y0=0,
            y1=1,
            fillcolor=color,
            opacity=0.1,
            line_width=1,
        )

        annotation = dict(
            showarrow=False,
            text=peak_name,
            textangle=90,
            x=time[peak.left],
            xanchor='left',
            xref='x3',
            y=1,
            yanchor='top',
            yref='y3 domain'
        )

        if shapes:
            fig['layout']['shapes'] += (vrect,)
        fig['layout']['annotations'] += (annotation,)

    return fig

def create_component_traces(fig: go.Figure, current_campaign: MoccaDataset, wl_idx: int, compounds: Dict[int, Compound]):
    """Creates traces that show concentrations of individual components"""

    chr_id = cache.get_displayed_chromatogram()

    peaks = current_campaign.chromatograms[chr_id].peaks
    time = current_campaign.time()
    assert time is not None

    for peak in peaks:
        peak_time = peak.time(time)
        for idx, component in enumerate(peak.components):
            if compounds[component.compound_id].name == '#ignore':
                continue

            compound = current_campaign.compounds[component.compound_id]

            color = plotly_colors.Alphabet[component.compound_id % len(plotly_colors.Alphabet)]

            fig.add_trace(
                go.Scatter(
                    x=peak_time,
                    y=component.concentration * compound.spectrum[wl_idx],
                    mode='lines',
                    name=f'Component {idx+1}',
                    line={'width': 1., 'color': color},
                    fill='tozeroy',
                    hoverinfo='none',
                ),
                row=2,
                col=1
            )

@callback(
    Output('results-figure-chromatogram', 'figure', allow_duplicate=True),
    Input("results-figure-chromatogram", "clickData"),
    prevent_initial_call='initial_duplicate'
)
def click(clickData):
    """Updates cross-section on the 2D chromatogram view"""
    if clickData is None:
        return Patch()

    # Using patch, only relevant data are updated, instead of passing entire figure back and forth
    fig = Patch()

    current_campaign = cache.get_campaign()

    subplot = clickData['points'][0]['curveNumber']
    t, wl = [clickData["points"][0][k] for k in ["x", "y"]]
    t_idx, t = current_campaign.closest_time(t)
    wl_idx, wl = current_campaign.closest_wavelength(wl)

    fig['layout']['annotations'] = [dict(
        font=dict(color='yellow', size=10),
        x=0,
        y=1.,
        showarrow=False,
        text=f"T: {t:0.3f}<br>WL: {wl:0.1f}",
        textangle=0,
        xanchor='left',
        xref="paper",
        yref="paper"
    )]

    add_peak_annotations(
        fig,
        current_campaign.chromatograms[cache.get_displayed_chromatogram(
        )].peaks,
        current_campaign.compounds,
        shapes=False
    )

    if subplot == subplots['heatmap']:
        fig = update_wl(fig, wl_idx, current_campaign)
        fig = update_time(fig, t_idx, current_campaign)
    elif subplot == subplots['chromatogram']:
        fig = update_time(fig, t_idx, current_campaign)
    elif subplot == subplots['spectrum']:
        fig = update_wl(fig, wl_idx, current_campaign)

    return fig


@callback(
    Output('results-figure-chromatogram', 'figure', allow_duplicate=True),
    Input("slider-chromatogram-limits", "value"),
    prevent_initial_call='initial_duplicate'
)
def update_heatmap_limits(limit):
    """Updates the limits of the chromatogram heatmap"""
    if limit is None:
        return Patch()

    current_campaign = cache.get_campaign()
    chr_id = cache.get_displayed_chromatogram()
    data = current_campaign.chromatograms[chr_id].data

    fig = Patch()
    fig['data'][subplots['heatmap']]['z'] = np.clip(data, None, limit)
    return fig
