from dash import html, dcc # type: ignore

from pages.home.description_text import all_text


def get_layout():
    """Returns the layout for the `home` page"""

    logo = html.Img(
        src="/assets/mocca_framed.png",
        alt="MOCCA logo",
        style={
            'height': '10rem',
            'width': 'auto',
            'align-self': 'center'
        })

    go_upload_data = html.P(
        ["If you already know what to do, you can start by ", html.A("UPLOADING DATA", href='/data')],
        className="lead align-self-center mt-5",
    )

    contents = [
        html.H1("WELCOME TO", className="text-body-secondary align-self-center mt-5 mb-3"),
        logo,
        go_upload_data,
        html.Hr(),
        dcc.Markdown(all_text, className="m-auto", style={'max-width':'80ch'}, link_target="_blank")
    ]

    return contents
