"""Generates layout for the `process` page"""

from dash import html, dcc  # type: ignore
from typing import Tuple

import cache

from pages.process.layout_settings_description import settings_description

# SETTINGS REFERENCE:
# baseline_smothness: float
# """Smoothness penalty for baseline"""
# min_rel_prominence: float
# """Minimal relative peak height"""
# border_max_peak_cutoff: float
# """Maximum relative peak height for peak cutoff"""
# split_threshold: float
# """Maximum relative height of minima between peaks to split them"""
# explained_threshold: float
# """Minimal R2 to consider peak resolved"""
# max_peak_distance: float
# """Maximum peak distance deviation [in time units] for one compound"""
# min_spectrum_correl: float
# """Minimum correlation of spectra for one compound"""
# min_elution_time: float
# """Peaks with maxima before this time will not be considered"""
# max_elution_time: float
# """Peaks with maxima after this time will not be considered"""
# min_wavelength: float = 220.
# """The data will be cropped such that lower wavelengths are not included"""
# max_wavelength: float = 600.
# """The data will be cropped such that higher wavelengths are not included"""


def get_label_and_input(text: str, id: str, value: float | None = None) -> Tuple:
    """Creates the html elements needed for entering config values"""
    label = html.Label(
        text,
        style={
            'text-align': 'right',
            'max-width': '35ch'
        }
    )

    input = dcc.Input(
        id=id,
        type="number",
        # persistence=True,
        # persistence_type="session",
        placeholder="",
        value=value,
        style={'max-width': '10ch', 'text-align': 'right'}
    )

    return label, input


def get_layout():
    """Generates layout for the `process` page"""

    current_campaign = cache.get_campaign()

    s = current_campaign.settings

    # Clip wavelenghts and elution times
    s.min_wavelength = max(s.min_wavelength, round(current_campaign.wavelength_raw()[0]))
    s.max_wavelength = min(s.max_wavelength, round(current_campaign.wavelength_raw()[-1]))

    s.min_elution_time = max(s.min_elution_time, round(current_campaign.time()[0], 2))
    s.max_elution_time = min(s.max_elution_time, round(current_campaign.time()[-1], 2))

    # Settings for MOCCA
    settings = html.Div(
        children=[
            html.H3("Spectrum Analysis Options", style={'grid-column': '1/3'}),
            html.Span('Cropping Wavelength', style={
                      'grid-column': '1/3', 'font-weight': 'bold'}),
            *get_label_and_input("Min Wavelength",
                                 "process-input-min-wavelength", s.min_wavelength),
            *get_label_and_input("Max Wavelength",
                                 "process-input-max-wavelength", s.max_wavelength),
            html.Small(f'available {current_campaign.wavelength_raw()[0]:0.0f} nm - {current_campaign.wavelength_raw()[-1]:0.0f} nm', style={
                      'grid-column': '1/3', 'font-weight': 'normal', 'text-align': 'right'}, className="text-secondary"),
            html.Span('Baseline Correction', style={
                      'grid-column': '1/3', 'font-weight': 'bold'}),
            *get_label_and_input("Baseline Smoothness",
                                 "process-input-baseline-smoothness", s.baseline_smoothness),
            html.Span('Peak Picking', style={
                      'grid-column': '1/3', 'font-weight': 'bold'}),
            *get_label_and_input("Min Peak Height",
                                 "process-input-min-prominence", s.min_prominence),
            *get_label_and_input("Min Relative Peak Height",
                                 "process-input-min-rel-prominence", s.min_rel_prominence),
            *get_label_and_input("Min Retention Time",
                                 "process-input-min-time", s.min_elution_time),
            *get_label_and_input("Max Retention Time",
                                 "process-input-max-time", s.max_elution_time),
            *get_label_and_input("Min Relative Peak Area",
                                 "process-input-min-rel-area", s.min_rel_integral),
            html.Small(f'available {current_campaign.time()[0]:0.2f} min - {current_campaign.time()[-1]:0.2f} min', style={
                      'grid-column': '1/3', 'font-weight': 'normal', 'text-align': 'right'}, className="text-secondary"),
            html.Span('Determining Peak Borders', style={
                      'grid-column': '1/3', 'font-weight': 'bold'}),
            *get_label_and_input("Max Peak Cutoff",
                                 "process-input-max-peak-cutoff", s.border_max_peak_cutoff),
            *get_label_and_input("Split Peaks Threshold",
                                 "process-input-split-thresh", s.split_threshold),
            html.Span('Deconvolution', style={
                      'grid-column': '1/3', 'font-weight': 'bold'}),
            *get_label_and_input("Min Peak Purity",
                                 "process-input-explained-thresh", s.explained_threshold),
            html.Span('Assigning Compounds', style={
                      'grid-column': '1/3', 'font-weight': 'bold'}),
            *get_label_and_input("Max Peak Distance",
                                 "process-input-max-dist-thresh", s.max_peak_distance),
            *get_label_and_input("Min Spectrum Correl",
                                 "process-input-min-spectrum-correl", s.min_spectrum_correl),

            html.Button(
                "Download",
                className='btn btn-outline-secondary',
                id='process-button-download-settings',
                style={'justify-self': 'end'}
            ),
            dcc.Upload(
                id='process-upload-settings',
                children=html.Button(
                    "Upload", className='btn btn-outline-secondary'),
                multiple=False
            ),
            dcc.Download(id="process-download-settings")
        ],
        style={
            'max-width': '60ch',
            'display': 'grid',
            'grid-template-columns': 'auto auto',
            'row-gap': '0.2em',
            'column-gap': '1ch'
        }
    )

    # Select input file for testing settins
    testinput = html.Div(
        style={
            'display': 'grid',
            'grid-template-columns': 'auto 1fr',
            'align-items': 'center',
            'column-gap': '2ch'
        },
        children=[
            html.Label(
                "Select one of the chromatogram sample files:",
            ),
            dcc.Dropdown(
                id='process-dropdown-single-test-sample',
                options={idx: chr.name for idx,
                         chr in current_campaign.chromatograms.items()},
                style={'width': '40ch'}
            )
        ]
    )

    plot_container = html.Div(id="process-div-chromatogram-container",style={'align-self':'stretch'})

    format_and_testinput = html.Div(
        children=[
            html.H3("Test settings on single sample", className="mt-5"),
            testinput,
            html.Button("Process Single Sample", id='process-button-process-single',
                        className='btn btn-outline-primary mt-1'),
            html.Span(id="process-span-process-single-message"),
            html.H3("Process Entire Dataset", className="mt-5"),
            html.P(
                "Once you are happy with the settings, you can process all files. This might take a while."),
            html.Button("Process All", id='process-button-process-all',
                        className='btn btn-outline-primary mt-1'),
            html.Span(id="process-span-process-all-message"),
            html.Hr(style={'align-self':'stretch'}),
            plot_container
        ],
        style={
            'display': 'flex',
            'flex-flow': 'column',
            'align-items': 'flex-start'
        }
    )

    upper_container = html.Div(
        children=[
            format_and_testinput,
            settings
        ],
        style={
            'display': 'grid',
            'grid-auto-flow': 'row',
            'grid-template-columns': '1fr auto',
        }
    )


    description = dcc.Markdown(settings_description)

    interval_updater = dcc.Interval(
        id='process-interval-background-updater',
        interval=500  # ms
    )

    return [upper_container, html.Hr(), description, interval_updater]
