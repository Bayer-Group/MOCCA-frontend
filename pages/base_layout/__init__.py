"""
Contains the layout shared between all pages, such as navbar and footer
"""

from dash import html, dcc # type: ignore

from pages.base_layout.layout_navbar import navbar

def get_layout() -> html.Div:
    """Returns the basic layout shared by all pages"""
    return html.Div(
        id="outermost-wrapper",
        children=[
            dcc.Location(id='url', refresh=False),
            navbar(),
            html.Div(
                id="page-content",
                className="px-5 pb-5 pt-3",
                style={
                    'display': 'flex',
                    'flex-flow': 'column',
                    'align-items': 'normal'
                })
        ])
