from dash import html, dcc, dash_table # type: ignore
import pandas as pd # type: ignore

import cache

def create_table() -> pd.DataFrame:
    """Creates dataframe with summary of all compounds"""
    current_campaign = cache.get_campaign()

    time = current_campaign.time()
    wavelength = current_campaign.wavelength()
    assert time is not None and wavelength is not None
    names = []
    elution_time = []
    maxima = []
    ids = []

    for compound_id, compound in current_campaign.compounds.items():
        ids += [compound_id]
        names += [compound.name]
        elution_time += [time[compound.elution_time]]

        max = []
        for maximum, intensity in compound.absorption_maxima():
            if intensity > 0.7: 
                i = 's'
            elif intensity > 0.3:
                i = 'm'
            else:
                i = 'w'
            max += [f'{wavelength[maximum]:0.0f} ({i})']
        maxima += [', '.join(max)]

    df = pd.DataFrame(data={'ID': ids, 'Compound':names, 'Elution Time': elution_time, 'UV-VIS Maxima': maxima})

    return df

def layout():
    """Returns layout for the results tab with compounds"""

    compounds = cache.get_campaign().compounds
    if len(compounds) == 0:
        return "There aren't any compounds data to be shown!"

    table_data = create_table()

    header = html.H5(
        "Summary of detected compounds",
        className='d-inline-block',
        style={'margin-right':'1rem'}
    )

    clipboard = dcc.Clipboard(id='results-clipboard-compounds', className='d-inline-block')

    table = dash_table.DataTable(
        id='results-table-compounds',
        data=table_data.to_dict('records'),
        columns=[
            {
                'name': 'Compound',
                'id': 'Compound',
                'editable': True
            },
            {
                'name': 'Elution Time',
                'id': 'Elution Time',
                'type': 'numeric',
                'format': {'specifier': '.3f'}
            },
            {
                'name': 'UV-VIS Maxima',
                'id': 'UV-VIS Maxima',
            },
        ],
        style_cell={'textAlign':'left'},
        sort_action='native',
    )

    options = {idx: c.name for idx, c in compounds.items()}
    default = None if len(options) == 0 else 0

    spectrum_title = html.H5("Absorbance spectra of compounds", className='mt-3')

    input_select = html.Div(
        className="mt-2 mb-2",
        children=[
            html.Label("Select compound", htmlFor='results-dropdown-compound-spectrum'),
            dcc.Dropdown(
                id='results-dropdown-compound-spectrum',
                options=options,
                value=default
            )
        ],
        style={
            'display': 'grid',
            'grid-template-columns': 'auto 1fr',
            'align-items': 'center',
            'column-gap': '2ch',
        }
    )

    spectrum = dcc.Graph(id='results-graph-compound-absorption')

    layout = [
        header,
        clipboard,
        table, 
        spectrum_title,
        input_select,
        spectrum,
    ]
    return layout
