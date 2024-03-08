"""Creates layout for the data upload page"""

from typing import Tuple

from dash import html, dcc, dash_table # type: ignore
from campaign import gen_upload_table_from_campaign

explanation_of_table = """\
##### Explanation of Table Columns

**Sample Name**: Name of the sample

**Sample File**: The file name of the uploaded chromatogram

**Blank File**: The file name of the blank chromatogram used for baseline correction

**Compound Name**: If this chromatogram is a reference with known compound, please choose a name for the compound

**Concentration**: The concentration of the pure reference compound (if known)

**ISTD Concentration**: Concentration of ISTD (if present)

**Name of ISTD**: Specify name of the internal standard, if used. Use same name as in `Compound Name`

*Units of concentration*: The program can work with any units, but the same units must be used for all entries! Please write only the values into the table, e.g. *10.58* and not *10.58 uM*
"""


def data_table() -> Tuple[dash_table.DataTable, str]:
    """Generates the table containing all data about uploaded files"""

    data, istd = gen_upload_table_from_campaign()

    table = dash_table.DataTable(
        id='data-table-sample-data',
        columns=([
            # The columns with IDs are not explicitly specified, but must be included in the `data` variable!
            # {'id': 'chromatogram_id', 'name': 'Chromatogram ID', 'editable': False},
            # {'id': 'sample_id', 'name': 'Sample File ID', 'editable': False},
            # {'id': 'blank_id', 'name': 'Blank File ID', 'editable': False},
            {'id': 'name', 'name': 'Sample Name'},
            {'id': 'sample', 'name': 'Sample File', 'editable': False},
            {'id': 'blank', 'name': 'Blank File', 'editable': False},
            {'id': 'compound_name', 'name': 'Compound Name'},
            {'id': 'compound_conc', 'name': 'Concentration', 'type': 'numeric'},
            {'id': 'istd_conc', 'name': 'ISTD Concentration', 'type': 'numeric'}
        ]),
        data=data,
        editable=True,
        row_deletable=True,
        css=[{"selector": ".Select-menu-outer",
              "rule": "display: block !important"}],
        style_cell={
            'height': 'auto',
            'minWidth': '150px', 'width': '150px', 'maxWidth': '250px',
            'whiteSpace': 'normal', 'textAlign': 'left'
        },
        sort_action='native',
    )

    return table, istd


def upload_card(header: str, text: str, id: str, allow_multiple: bool = True) -> html.Div:
    """Generates the upload cards"""
    upl = dcc.Upload(
        id=id,
        className="cursor-pointer align-items-center row",
        children=html.Div(html.Small(text)),
        style={
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'height': '100%',
            'min-height': '40px',
        },
        # Allow multiple files to be uploaded
        multiple=allow_multiple
    )

    card = html.Div(
        className="card bg-light col",
        children=[
            html.Div(
                header,
                className="card-header"
            ),
            html.Div(
                className="card-body row",
                children=[
                    upl
                ]
            )
        ]
    )
    return card


def get_layout():
    """Returns the layout"""
    # Upload cards
    upload_cards = html.Div(
        className="row gap-4",
        children=[
            upload_card("Load Campaign", "Restore a previous campaign from .pkl file",
                        "data-upload-campaign", allow_multiple=False),
            upload_card("Select Blank", "Select the chromatogram with gradient only to use as blank",
                        "data-upload-blank", allow_multiple=False),
            upload_card("Upload Sample", "Select the chromatogram data for analysis",
                        "data-upload-sample")
        ]
    )

    # Current blank
    current_blank = html.Div(
        className="row",
        children=[
            html.Span("Currently selected blank:", className="col-md-auto"),
            html.Span(
                "NO BLANK SELECTED - select blank before uploading samples",
                id="data-span-uploaded-blank-message",
                className="text-warning col"
            )
        ]
    )

    table_header = html.H3(
        "Please add information about the uploaded chromatograms",
        className="mt-5"
    )

    # Table with uploaded files
    table, istd = data_table()

    # Name of ISTD
    choose_istd = html.Div(
        [
            html.Label("Name of ISTD:", htmlFor="data-input-istd"),
            dcc.Input(value=istd, id='data-input-istd')
        ],
        style={
            'display': 'flex',
            'gap': '2ch',
            'margin': '0.5rem 0'
        }
    )

    # Action buttons - confirm data, discard changes, download campaign
    buttons = html.Div(
        className="row row-cols-auto mt-3 mb-1 justify-content-evenly",
        children=[
            html.Button(
                "Download Campaign",
                id="data-button-download-campaign",
                className="btn btn-outline-primary"
            ),
            html.Button(
                "Discard Changes",
                id="data-button-discard-changes",
                className="btn btn-outline-danger"
            ),
            html.Button(
                "Confirm Changes",
                id="data-button-confirm-changes",
                className="btn btn-outline-success"
            )
        ]
    )

    buttons_log = html.Span(
        id="data-span-buttons-message",
        className=""
    )

    explanation = dcc.Markdown(explanation_of_table)

    layout = [
        upload_cards,
        current_blank,
        table_header,
        table,
        choose_istd,
        buttons,
        buttons_log,
        html.Hr(className="mt-5 mb-3"),
        explanation,
        dcc.Download(id="data-button-download-campaign-pkl")
    ]

    return layout
