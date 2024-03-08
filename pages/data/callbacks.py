from dash import Input, Output, State, callback, dcc # type: ignore

import cache
import campaign


@callback(
    output=[
        Output('data-span-uploaded-blank-message', 'children'),
        Output('data-span-uploaded-blank-message', 'className')
    ],
    inputs=[Input('data-upload-blank', 'contents')],
    state=[State('data-upload-blank', 'filename')],
)
def upload_blank(content, name):
    """Handles upload of blank chromatogram file"""
    if content is not None:
        fileid = cache.save_uploaded_file(name, content)
        cache.set_current_blank(fileid)

    blank_id = cache.get_current_blank()
    if blank_id is None:
        return "NO BLANK SELECTED - select blank before uploading samples", "text-warning col"
    else:
        blank = cache.get_cached_file(blank_id)
        return blank.original_name, "text-success col"


@callback(
    output=[
        Output('data-table-sample-data', 'data', allow_duplicate=True),
        Output('data-span-buttons-message', 'children', allow_duplicate=True),
        Output('data-span-buttons-message', 'className', allow_duplicate=True)
    ],
    inputs=[Input('data-upload-sample', 'contents')],
    state=[
        State('data-upload-sample', 'filename'),
        State('data-table-sample-data', 'data')
    ],
    prevent_initial_call=True
)
def upload_sample(contents, names, rows):
    """Handles upload of sample chromatogram files"""
    if contents is not None:
        for name, content in sorted(zip(names, contents)):
            blank_id = cache.get_current_blank()

            sample_id = cache.save_uploaded_file(name, content)

            if blank_id is None:
                blank_name = "No blank selected!"
            else:
                blank_name = cache.get_cached_file(blank_id).original_name

            sample_names = {r['name'] for r in rows}
            name_idx = 1
            name = f'Sample {name_idx}'
            while name in sample_names:
                name_idx += 1
                name = f'Sample {name_idx}'

            data = dict(
                chromatogram_id=None,
                sample_id=sample_id,
                blank_id=blank_id,
                name=name,
                sample=cache.get_cached_file(sample_id).original_name,
                blank=blank_name,
                compound_name="",
                compound_conc="",
                istd_conc=""
            )
            rows.append(data)

    return rows, "Don't forget to confirm the changes!", "text-warning"


@callback(
    output=[
        Output('data-table-sample-data', 'data', allow_duplicate=True),
        Output('data-input-istd', 'value', allow_duplicate=True),
        Output('data-span-buttons-message', 'children', allow_duplicate=True),
        Output('data-span-buttons-message', 'className', allow_duplicate=True)
    ],
    inputs=[Input('data-upload-campaign', 'contents')],
    state=[
        State('data-table-sample-data', 'data'),
        State('data-input-istd', 'value'),
    ],
    prevent_initial_call=True
)
def upload_campaign(content, old_rows, old_istd):
    """Handles upload of sample chromatogram files"""
    if content is not None:
        try:
            # Save the file in cache folder
            file_id = cache.save_uploaded_file('campaign.pkl', content)
            # Unpickle the file
            campaign.unpickle_all(file_id)
            # Generate the data for upload table
            rows, istd = campaign.gen_upload_table_from_campaign()
        except Exception as ex:
            return old_rows, old_istd, "An error occured during uploading or parsing the campaign file. "+str(ex), "text-danger"

        return rows, istd, "The campaign has been loaded successfuly!", "text-success"

    return old_rows, old_istd, "No file has been selected...", "text-warning"


@callback(
    output=[
        Output('data-span-buttons-message', 'children', allow_duplicate=True),
        Output('data-span-buttons-message', 'className', allow_duplicate=True)
    ],
    inputs=[Input('data-button-confirm-changes', 'n_clicks'),],
    state=[
        State('data-table-sample-data', 'data'),
        State('data-input-istd', 'value')
    ],
    prevent_initial_call=True
)
def confirm_changes(_, rows, istd):
    """Reads the data from the upload table and creates the MOCCA campaign"""
    try:
        campaign.campaign_from_table(rows, istd)
    except Exception as ex:
        raise ex
        return "Error!" + str(ex), "text-danger"
    
    
    current_campaign = cache.get_campaign()
    if len(current_campaign.chromatograms) == 0:
        return "Campaign updated successfuly, but there aren't any HPLC data!", "text-warning"
    else:
        return "Campaign updated successfuly! You can now process your data", "text-success"


@callback(
    output=[
        Output('data-button-download-campaign-pkl', 'data'),
        Output('data-span-buttons-message', 'children', allow_duplicate=True),
        Output('data-span-buttons-message', 'className', allow_duplicate=True),
    ],
    inputs=[Input('data-button-download-campaign', 'n_clicks')],
    prevent_initial_call=True
)
def download_campaign(_):
    """Pickles and downloads the current MOCCA campaign """
    print("Pickling the campaign")
    path = campaign.pickle_all()
    print("Sending pickled campaign")

    return dcc.send_file(path, 'campaign.pkl'), "The campaign is downloading...", "text-success"


@callback(
    output=[
        Output('data-table-sample-data', 'data'),
        Output('data-input-istd', 'value'),
        Output('data-span-buttons-message', 'children', allow_duplicate=True),
        Output('data-span-buttons-message', 'className', allow_duplicate=True),
    ],
    inputs=[Input('data-button-discard-changes', 'n_clicks')],
    prevent_initial_call=True
)
def discard_changes(_):
    """Discards new changes and reloads the previously confirmed campaign"""

    table, istd = campaign.gen_upload_table_from_campaign()

    return table, istd, "The changes has been discarded and previous campaign was loaded!", "text-success"
