from dash import html, dcc, dash_table # type: ignore

from pages.results import callbacks_integrals

import cache




def layout_integrals():
    df = callbacks_integrals.get_integrals_dataframe()
    cols = callbacks_integrals.get_columns(df, 1)
    rows = df.to_dict('records')

    header = html.H5(
        "Absolute absorbance integrals",
        className='d-inline-block',
        style={'margin-right': '1rem'}
    )

    clipboard = dcc.Clipboard(
        id='results-clipboard-integrals', className='d-inline-block')

    table = html.Div(
        dash_table.DataTable(
            id='results-table-integrals',
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


def layout_rel_integrals():
    if cache.get_campaign().istd_compound is None:
        return """The current campaign does not have any internal standard!"""
    df = callbacks_integrals.get_rel_integrals_dataframe()
    cols = callbacks_integrals.get_columns(df, 1)
    rows = df.to_dict('records')

    header = html.H5(
        "Absorbance integrals normalized against internal standard",
        className='d-inline-block',
        style={'margin-right': '1rem'}
    )

    clipboard = dcc.Clipboard(
        id='results-clipboard-rel-integrals', className='d-inline-block')

    table = html.Div(
        dash_table.DataTable(
            id='results-table-rel-integrals',
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
