"""
This is the entry point for the Dash application
"""

import dash # type: ignore
import dash_bootstrap_components as dbc # type: ignore
import webbrowser

# This is for caching global variables
from flask_caching import Cache

# Do not print request logs
import logging
logging.getLogger('werkzeug').setLevel(logging.WARNING)

# bootstrap theme (https://bootswatch.com/cerulean/)
external_stylesheets = [dbc.themes.CERULEAN]
external_scripts = [{
        'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js',
        'integrity': 'sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p',
        'crossorigin': 'anonymous'
    }]

# initialize the application
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    title="Mocca"
)
server = app.server

# this suppresses exceptions when html elements accessed by callbacks were not created yet
app.config.suppress_callback_exceptions = True

# Initialize cache - needed for global variables
flask_cache = Cache()
flask_cache.init_app(app.server, config={'CACHE_TYPE':'SimpleCache', "CACHE_DEFAULT_TIMEOUT":1e30})

# define directory for caching files
CACHE_DIR = '_cache'

# Pages must be imported after cache and campaign are initialized
import cache
import campaign

import pages
import pages.base_layout
import pages.home
import pages.data
import pages.process
import pages.results

# create callback for loading content for different URL paths
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname : str):
    """
    When URL changes, the content of `div#page-content` is updated accordingly
    """
    if pathname in ['', '/', '/home']:
        return pages.home.get_layout()
    elif pathname == "/data":
        return pages.data.get_layout()
    elif pathname == "/process":
        return pages.process.get_layout()
    elif pathname == "/results":
        return pages.results.get_layout()
    else:
        # TODO: add page not found page
        return None 

@app.server.before_first_request
def initialize():
    # initialize global variables and file caching
    cache.init()

    # load the base layout
    app.layout = pages.base_layout.get_layout()

# start the server
if __name__ == '__main__':
    # app.run(host='127.0.0.1', debug=True)

    #webbrowser.open_new("http://localhost:8050")
    app.run(host='127.0.0.1', debug=True)
