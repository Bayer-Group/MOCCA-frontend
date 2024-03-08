"""
Definition of the navbar for all pages
"""

from dash import html # type: ignore


def navbar():
    """Returns the navbar element"""
    # contains (text, href, id)
    buttons = [
        ("Home", "/home", "nav-home"),
        ("Data", "/data", "nav-data"),
        ("Process", "/process", "nav-process"),
        ("Results", "/results", "nav-results")
    ]

    # create navbar
    navbar = html.Nav(
        className="navbar navbar-expand-lg bg-primary", children=[
            html.Div(className="container-fluid", children=[])
        ]
    )

    # add mocca logo
    navbar.children[0].children.append(
        html.A(
            className="navbar-brand row align-items-center",
            href="/home",
            children=[
                html.Img(
                    className="col",
                    src="/assets/mocca_framed.png",
                    alt="MOCCA logo",
                    height="50"),
                html.H6(
                    ["Multivariate Online", html.Br(), "Contextual Chromatographic Analysis"],
                    className="text-body-secondary col mb-0"
                )
            ]
        )
    )

    # add button for collapsing
    navbar.children[0].children.append(
        html.Button(
            className="navbar-toggler",
            children=[
                html.Span(className="navbar-toggler-icon")
            ],
            **{
                "type": "button",
                "data-bs-toggle": "collapse",
                "data-bs-target": "#navbarSupportedContent",
                "aria-controls": "navbarSupportedContent",
                "aria-expanded": "false",
                "aria-label": "Toggle navigation"}
        )
    )

    # add links
    navbar.children[0].children.append(
        html.Div(
            className="collapse navbar-collapse justify-content-end",
            id="navbarSupportedContent",
            children=[
                html.Ul(
                    className="navbar-nav",
                    children=[
                        html.Li(className="nav-item px-2", children=[
                            html.A(btn[0], className="nav-link px-2", href=btn[1], id=btn[2])])
                        for btn in buttons
                    ]
                )
            ])
    )

    return navbar
