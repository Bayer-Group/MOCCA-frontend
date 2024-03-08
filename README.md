# Frontend web app for MOCCA

### Installation
Get the latest MOCCA from `!!! TO DO !!!`.

Install Python (3.11.4 has been tested) and the packages according to requirements.txt (`pip install -r requirements.txt`).

Make sure Python can find the MOCCA package, ideally by adding `[PARENT DIR]/!!! TO DO !!!/src` to `PYTHONPATH`.

Start the application by `python app.py` or using the `run.bat` file. The frontend can be then accessed from `http://localhost:8050/`.

### Compiling to executable

Run `pyinstaller app.spec`. The executable should be created in `dist/mocca.exe`.

# Code Standards
This section describes the directory structure, file structure, naming of variables, and overall standards for the code.

### Directory Structure
The entry point is `app.py`, Dash pages are in `pages/[page_name]`,
all campaign data and relevant functions are in `campaign/`,
and global variables and local files are handled in `cache/`.

Each **page** folder contains the following:
 * `__init__.py` file with `layout()` function
 * all functions that generate layout must be in files `layout*.py`
 * all callbacks must be in files `callbacks*.py`
 * other functions (data processing, parsing) should be in separate files

### Code standards
Imports are in following order:
 * `dataclasses` and `typing`
 * imports from external packages
 * imports from `mocca`
 * imports from this project

All classes shoud use `dataclass`, attributes must be typed and have description.

Functions should be typed (both parameters and return type), and contain description. This may not be neccessary for small helper functions...

### Global variables and cached files
Global variables must be stored in flask cache - this is also neccessary because of how the server works. The variables should be accessed and modified only through functions `cache.get_[variable_name]()` and `cache.set_[variable_name]()`. This helps with typing and prevents spelling mistakes.

Cached files can be stored in the `_cache` folder. All information about the cached files must be in `cache.files`.

_Note that the current implementation is not suitable for having multiple clients - file cache needs to be changed later!_

### Running background jobs
The background callbacks provided by Dash don't work very well with flask-cache and are slow.

Background jobs are thus done using python `threading` and the `Interval` component.

# Naming variables
All IDs of html components must be `[page-name]-[component-type]-[anything else]`, for example `process-dropdown-input-file-type`.