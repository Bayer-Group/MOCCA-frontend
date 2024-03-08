from dash import html, dcc # type: ignore

def get_layout():
    tab_style = {'padding':'0.5rem'}
    tabs = dcc.Tabs(
        id="results-tabs",
        value='area_perc',
        children=[
            dcc.Tab(label='Area %', value='area_perc', style=tab_style, selected_style=tab_style),
            dcc.Tab(label='Concentrations', value='conc', style=tab_style, selected_style=tab_style),
            dcc.Tab(label='Concentrations (ISTD)', value='conc_istd', style=tab_style, selected_style=tab_style),
            dcc.Tab(label='Chromatograms', value='chromatograms', style=tab_style, selected_style=tab_style),
            dcc.Tab(label='Compounds', value='compounds', style=tab_style, selected_style=tab_style),
        ],
    )

    layout = [
        tabs,
        html.Div(
            id='results-div-tabs-content',
            style={'height': '100%', 'width': '100%'},
            className='mt-3'
        ),
    ]

    return layout


