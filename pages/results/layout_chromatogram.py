from dash import html, dcc, callback, Input, Output, Patch, State # type: ignore

import cache
from pages.results.layout_chrom_fig import create_figure

def layout():
    current_campaign = cache.get_campaign()
    select_options = {idx: ch.name for idx, ch in current_campaign.chromatograms.items()}
    default = None if len(select_options) == 0 else list(select_options.keys())[0]
    cache.set_displayed_chromatogram(default)

    input_select = html.Div(
        className="mt-2 mb-2",
        children=[
            html.Label("Select chromatogram file", htmlFor='results-dropdown-chromatogram-for-visualization'),
            dcc.Dropdown(
                id='results-dropdown-chromatogram-for-visualization',
                options=select_options,
                value = default
            )
        ],
        style={
            'display': 'grid',
            'grid-template-columns': 'auto 1fr',
            'align-items': 'center',
            'column-gap': '2ch',
        }
    )

    if default is not None:
        layout = [
            input_select,
            create_figure(only_figure=False)
        ]
    else:
        layout = ["There aren't any chromatograms to show!"]

    return layout

@callback(
    Output('results-figure-chromatogram', 'figure', allow_duplicate=True),
    Input("results-dropdown-chromatogram-for-visualization", "value"),
    State('results-figure-chromatogram', 'figure'),
    prevent_initial_call=True
)
def change_chromatogram_callback(chromatogram_id, fig):
    """Changes the shown chromatogram on the results page"""
    if chromatogram_id is None:
        return Patch()
    
    chromatogram_id = int(chromatogram_id)
    
    cache.set_displayed_chromatogram(chromatogram_id)
    fig = create_figure()

    return fig