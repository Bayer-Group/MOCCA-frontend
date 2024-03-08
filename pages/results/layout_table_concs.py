from dash import html, dcc, dash_table # type: ignore

from pages.results import callbacks_concs

import cache


def layout_area_perc():
    select_wavelength = html.Div(
        [
            html.Label("Select wavelength:"),
            dcc.Input(
                id='input-wavelength-for-area',
                value=230,
                type='number',
                persistence=True,
                persistence_type="session",
            ),
            html.Button(
                "Confirm",
                className="btn btn-outline-primary",
                id='button-set-wavelength-for-area'
            ),
        ],
        style={
            'display': 'flex',
            'flex-flow': 'row',
            'align-items': 'center',
            'margin-bottom': '1rem',
            'gap': '2ch',
        }
    )

    header = html.H5(
        id='results-h5-area-percent-wavelength',
        className='d-inline-block',
        style={'margin-right': '1rem'}
    )

    clipboard = dcc.Clipboard(
        id='results-clipboard-area-percent', className='d-inline-block')

    table = html.Div(
        dash_table.DataTable(
            id='results-table-area-percent',
            data=[],
            columns=[],
            style_cell_conditional=[{
                'if': {'column_id': 'Chromatogram'},
                'textAlign': 'left'
            }],
            sort_action='native',
        ),
        style={'width': '100%', 'overflow-x': 'auto'}
    )

    return [select_wavelength, header, clipboard, table]


def layout_conc():
    df = callbacks_concs.get_concs_abs_dataframe()
    cols = callbacks_concs.get_columns(df, 1)
    rows = df.to_dict('records')

    header = html.H5(
        "Absolute absorbance integrals",
        className='d-inline-block',
        style={'margin-right': '1rem'}
    )

    clipboard = dcc.Clipboard(
        id='results-clipboard-conc-abs', className='d-inline-block')

    table = html.Div(
        dash_table.DataTable(
            id='results-table-conc-abs',
            data=rows,
            columns=cols,
            style_cell_conditional=[{
                'if': {'column_id': 'Chromatogram'},
                'textAlign': 'left'
            }],
            sort_action='native',
        ),
        style={'width': '100%', 'overflow-x': 'auto'}
    )

    return header, clipboard, table


def layout_conc_istd():
    if cache.get_campaign().istd_compound is None:
        return """The current campaign does not have any internal standard!"""
    df = callbacks_concs.get_concs_istd_dataframe()
    cols = callbacks_concs.get_columns(df, 1)
    rows = df.to_dict('records')

    header = html.H5(
        "Absorbance integrals normalized against internal standard",
        className='d-inline-block',
        style={'margin-right': '1rem'}
    )

    clipboard = dcc.Clipboard(
        id='results-clipboard-conc-istd', className='d-inline-block')

    table = html.Div(
        dash_table.DataTable(
            id='results-table-conc-istd',
            data=rows,
            columns=cols,
            style_cell_conditional=[{
                'if': {'column_id': 'Chromatogram'},
                'textAlign': 'left'
            }],
            sort_action='native',
        ),
        style={'width': '100%', 'overflow-x': 'auto'}
    )

    return header, clipboard, table
