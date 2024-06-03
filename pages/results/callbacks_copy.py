from dash import callback, Input, Output, State # type: ignore
import pandas as pd # type: ignore

@callback(
    Output('results-clipboard-area-percent','content'),
    Input('results-clipboard-area-percent', 'n_clicks'),
    State('results-table-area-percent', 'data'),
    prevent_initial_callback=True
)
def copy_table_to_clipboard_area(_, data):
    df = pd.DataFrame(data)
    return df.to_csv(index=False, sep='\t', decimal=',')

@callback(
    Output('results-clipboard-conc-abs','content'),
    Input('results-clipboard-conc-abs', 'n_clicks'),
    State('results-table-conc-abs', 'data'),
    prevent_initial_callback=True
)
def copy_table_to_clipboard_conc(_, data):
    df = pd.DataFrame(data)
    return df.to_csv(index=False, sep='\t', decimal=',')

@callback(
    Output('results-clipboard-conc-istd','content'),
    Input('results-clipboard-conc-istd', 'n_clicks'),
    State('results-table-conc-istd', 'data'),
    prevent_initial_callback=True
)
def copy_table_to_clipboard_istd(_, data):
    df = pd.DataFrame(data)
    return df.to_csv(index=False, sep='\t', decimal=',')

@callback(
    Output('results-clipboard-compounds','content'),
    Input('results-clipboard-compounds', 'n_clicks'),
    State('results-table-compounds', 'data'),
    prevent_initial_callback=True
)
def copy_table_to_clipboard_compounds(_, data):
    df = pd.DataFrame(data)
    return df.to_csv(index=False, sep='\t', decimal=',')

@callback(
    Output('results-clipboard-integrals','content'),
    Input('results-clipboard-integrals', 'n_clicks'),
    State('results-table-integrals', 'data'),
    prevent_initial_callback=True
)
def copy_table_to_clipboard_integrals(_, data):
    df = pd.DataFrame(data)
    return df.to_csv(index=False, sep='\t', decimal=',')

@callback(
    Output('results-clipboard-rel-integrals','content'),
    Input('results-clipboard-rel-integrals', 'n_clicks'),
    State('results-table-rel-integrals', 'data'),
    prevent_initial_callback=True
)
def copy_table_to_clipboard_rel_integrals(_, data):
    df = pd.DataFrame(data)
    return df.to_csv(index=False, sep='\t', decimal=',')