from dash import Input, Output, State, callback, html # type: ignore
from dash.exceptions import PreventUpdate # type: ignore
import threading
import base64

from mocca2.dataset import ProcessingSettings

from pages.process.process_single import process_single
import cache
from cache import CampaignProcessingInfo


@callback(
    output=[
        Output('process-span-process-single-message',
               'children', allow_duplicate=True),
        Output('process-span-process-single-message',
               'className', allow_duplicate=True),
        Output('process-button-process-single',
               'disabled', allow_duplicate=True)
    ],
    inputs=[Input('process-button-process-single', 'n_clicks')],
    state=[State('process-button-process-single', 'disabled')],
    prevent_initial_call=True
)
def disable_process_single_button(_, disabled):
    """Disables the button and triggers the process_single_hplc callback"""
    if not disabled:
        return "The sample is being processed...", "text-warning", True
    else:
        raise PreventUpdate()


@callback(
    output=[
        Output('process-div-chromatogram-container', 'children'),
        Output('process-span-process-single-message',
               'children', allow_duplicate=True),
        Output('process-span-process-single-message',
               'className', allow_duplicate=True),
        Output('process-button-process-single',
               'disabled', allow_duplicate=True)
    ],
    inputs=[
        Input('process-button-process-single', 'disabled')
    ],
    state=[
        State('process-dropdown-single-test-sample', 'value'),
        State('process-input-min-rel-prominence', 'value'),
        State('process-input-max-peak-cutoff', 'value'),
        State('process-input-split-thresh', 'value'),
        State('process-input-explained-thresh', 'value'),
        State('process-input-max-dist-thresh', 'value'),
        State('process-input-min-spectrum-correl', 'value'),
        State('process-input-min-time', 'value'),
        State('process-input-max-time', 'value'),
        State('process-input-baseline-smoothness', 'value'),
        State('process-input-min-prominence', 'value'),
        State('process-input-min-wavelength', 'value'),
        State('process-input-max-wavelength', 'value'),
        State('process-input-min-rel-area', 'value'),
    ],
    prevent_initial_call=True
)
def process_single_hplc(disabled, sample_index: int, *args: float):
    """One HPLC input is processed and visualized to test the MOCCA settings"""

    if not disabled:
        raise PreventUpdate()

    if sample_index is None:
        return [], f"Please select which sample to process!", "text-danger", False
    
    sample_index = int(sample_index)

    settings = ProcessingSettings(
        min_rel_prominence=args[0],
        border_max_peak_cutoff=args[1],
        split_threshold=args[2],
        explained_threshold=args[3],
        max_peak_distance=args[4],
        min_spectrum_correl=args[5],
        min_elution_time=args[6],
        max_elution_time=args[7],
        baseline_smoothness=args[8],
        min_prominence=args[9],
        min_wavelength=args[10],
        max_wavelength=args[11],
        min_rel_integral=args[12]
    )

    result = process_single(settings, sample_index)

    if type(result) is str:
        return "", result, "text-danger", False
    
    current_campaign = cache.get_campaign()
    sample_name = current_campaign.chromatograms[sample_index].name

    layout = [
        html.H5(f"Preview of {sample_name}:", className='mt-3'),
        result
    ]

    return layout, f"The sample `{sample_name}` is shown below!", "text-success", False


@callback(
    output=[
        Output('process-span-process-all-message',
               'children', allow_duplicate=True),
        Output('process-span-process-all-message',
               'className', allow_duplicate=True),
        Output('process-button-process-all', 'disabled', allow_duplicate=True)
    ],
    inputs=[
        Input('process-button-process-all', 'n_clicks')
    ],
    state=[
        State('process-input-min-rel-prominence', 'value'),
        State('process-input-max-peak-cutoff', 'value'),
        State('process-input-split-thresh', 'value'),
        State('process-input-explained-thresh', 'value'),
        State('process-input-max-dist-thresh', 'value'),
        State('process-input-min-spectrum-correl', 'value'),
        State('process-input-min-time', 'value'),
        State('process-input-max-time', 'value'),
        State('process-input-baseline-smoothness', 'value'),
        State('process-input-min-prominence', 'value'),
        State('process-input-min-wavelength', 'value'),
        State('process-input-max-wavelength', 'value'),
        State('process-input-min-rel-area', 'value'),
    ],
    prevent_initial_call=True,
)
def process_all_hplc(_, *args: float):
    """This processes all HPLC inputs using MOCCA"""

    settings = ProcessingSettings(
        min_rel_prominence=args[0],
        border_max_peak_cutoff=args[1],
        split_threshold=args[2],
        explained_threshold=args[3],
        max_peak_distance=args[4],
        min_spectrum_correl=args[5],
        min_elution_time=args[6],
        max_elution_time=args[7],
        baseline_smoothness=args[8],
        min_prominence=args[9],
        min_wavelength=args[10],
        max_wavelength=args[11],
        min_rel_integral=args[12]
    )

    # If the campaign is currently processed, don't process it again
    if cache.get_campaign_processing_info().status != 'IDLE':
        raise PreventUpdate()
    
    cache.set_campaign_processing_info(
        CampaignProcessingInfo(
            status='PROCESSING',
            message="",
            message_class=""
        )
    )

    # Explicit threading is used instead of Dash background callbacks, because:
    # 1. the DiskCache callbacks are really slow
    # 2. sharing state (flask-cache) with background callbacks is not trivial
    def process_all(settings):
        try:
            current_campaign = cache.get_campaign()
            current_campaign.process_all(settings)
            cache.set_campaign(current_campaign)
            message = "Data has been processed successfuly! You can now go to results", "text-success"
        except Exception as ex:
            message = str(ex), "text-danger"

        cache.set_campaign_processing_info(
            CampaignProcessingInfo(
                status='NEW_DATA_READY',
                message=message[0],
                message_class=message[1]
            )
        )

    threading.Thread(target=process_all, args=[settings]).start()

    return "The data is being processed, please wait...", "text-warning", True


@callback(
    output=[
        Output('process-span-process-all-message',
               'children', allow_duplicate=True),
        Output('process-span-process-all-message',
               'className', allow_duplicate=True),
        Output('process-button-process-all', 'disabled', allow_duplicate=True)
    ],
    inputs=[
        Input('process-interval-background-updater', 'n_intervals')
    ],
    prevent_initial_call=True
)
def update_background_results(_):
    """Checks whether background tasks have finished and updates GUI accordingly"""

    processing_info = cache.get_campaign_processing_info()
    if processing_info.status != 'NEW_DATA_READY':
        raise PreventUpdate()
    
    processing_info.status='IDLE'
    cache.set_campaign_processing_info(processing_info)
    
    return processing_info.message, processing_info.message_class, False


@callback(
    Output('process-download-settings', 'data'),
    inputs=Input('process-button-download-settings', 'n_clicks'),
    state=[
        State('process-input-min-rel-prominence', 'value'),
        State('process-input-max-peak-cutoff', 'value'),
        State('process-input-split-thresh', 'value'),
        State('process-input-explained-thresh', 'value'),
        State('process-input-max-dist-thresh', 'value'),
        State('process-input-min-spectrum-correl', 'value'),
        State('process-input-min-time', 'value'),
        State('process-input-max-time', 'value'),
        State('process-input-baseline-smoothness', 'value'),
        State('process-input-min-prominence', 'value'),
        State('process-input-min-wavelength', 'value'),
        State('process-input-max-wavelength', 'value'),
        State('process-input-min-rel-area', 'value'),
    ],
    prevent_initial_call=True
)
def download_settings(_, *args):
    """Downloads current settings as yaml"""
    
    settings = ProcessingSettings(
        min_rel_prominence=args[0],
        border_max_peak_cutoff=args[1],
        split_threshold=args[2],
        explained_threshold=args[3],
        max_peak_distance=args[4],
        min_spectrum_correl=args[5],
        min_elution_time=args[6],
        max_elution_time=args[7],
        baseline_smoothness=args[8],
        min_prominence=args[9],
        min_wavelength=args[10],
        max_wavelength=args[11],
        min_rel_integral=args[12]
    )

    return dict(content=settings.to_yaml(), filename="settings.yaml")

@callback(
    output=[
        Output('process-input-min-rel-prominence', 'value'),
        Output('process-input-max-peak-cutoff', 'value'),
        Output('process-input-split-thresh', 'value'),
        Output('process-input-explained-thresh', 'value'),
        Output('process-input-max-dist-thresh', 'value'),
        Output('process-input-min-spectrum-correl', 'value'),
        Output('process-input-min-time', 'value'),
        Output('process-input-max-time', 'value'),
        Output('process-input-baseline-smoothness', 'value'),
        Output('process-input-min-prominence', 'value'),
        Output('process-input-min-wavelength', 'value'),
        Output('process-input-max-wavelength', 'value'),
        Output('process-input-min-rel-area', 'value'),
    ],
    inputs=Input('process-upload-settings', 'contents'),
    prevent_initial_call=True
)
def upload_settings(content):
    """Reads settings from the uploaded yaml file"""
    
    if content is None:
        raise PreventUpdate()
    
    # try:
    _, content_string = content.split('base64,')
    decoded = base64.b64decode(content_string).decode()
    settings = ProcessingSettings.from_yaml(decoded)
    # except:
    #     print("Error while uploading settings")
    #     raise PreventUpdate()

    vals = [
        settings.min_rel_prominence,
        settings.border_max_peak_cutoff,
        settings.split_threshold,
        settings.explained_threshold,
        settings.max_peak_distance,
        settings.min_spectrum_correl,
        settings.min_elution_time,
        settings.max_elution_time,
        settings.baseline_smoothness,
        settings.min_prominence,
        settings.min_wavelength,
        settings.max_wavelength,
        settings.min_rel_integral
    ]

    return vals