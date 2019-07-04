import dash_html_components as html
from dash_callback_conglomerate import Router, PartialUpdate
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash

app = dash.Dash(__name__)
router = Router(app, True)

app.layout = html.Div([
    html.H1('1', id='text1'),
    html.H1('2', id='text2'),
    html.Button('Button 1', id='button1'),
    html.Button('Button 2', id='button2'),
    html.Button('Button 3', id='button3')
])


# Explicitly calling the router callback function
# Update text1 when button1 are button2 is pressed with the sum of all button presses
# PreventUpdate still works for the individual callback
@router.callback([Output('text1', 'children'),
                  Output('text2', 'children')],
                 [Input('button1', 'n_clicks'),
                  Input('button2', 'n_clicks')],
                 [State('button3', 'n_clicks')])
def button1(clicks1, clicks2, clicks3):
    if not clicks1 and not clicks2 and not clicks3:
        raise PreventUpdate()
    raise PartialUpdate({'text1.children': 'Partial Output: {}'.format(
        (clicks1 if clicks1 else 0) + (clicks2 if clicks2 else 0) + (clicks3 if clicks3 else 0))})


# Implicitly calling router callback function
# Tuples work for returning values
@app.callback([Output('text1', 'children'),
               Output('text2', 'children')],
              [Input('button2', 'n_clicks')])
def button2(clicks2):
    raise PartialUpdate({'text2.children': clicks2})


# Intended helper functions for often returned value pairs
def set_all_text_update(value, return_dict=None):
    if not return_dict:
        return_dict = {}
    return_dict['text1.children'] = value
    return_dict['text2.children'] = value
    return return_dict


# Returning all outputs in a list works
@app.callback([Output('text1', 'children'),
               Output('text2', 'children')],
              [Input('button3', 'n_clicks')])
def button3(clicks3):
    if clicks3 and clicks3 > 4:
        raise PartialUpdate(set_all_text_update(clicks3, {}))  # Pass any other outputs into helper function
    return ['0', '0']


# Call when you are done assigning callbacks
router.register_callbacks()

if __name__ == '__main__':
    app.run_server(debug=True)
