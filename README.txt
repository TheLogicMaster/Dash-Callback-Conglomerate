This is a Plotly Dash add-on for enabling more freedom with callback handling, enabling sharing inputs, outputs, and
only returning some of the outputs registered for a callback. There are two ways to use this add-on. One method is
seamless integration where the dash callback function is hijacked and replaced with a call to this modules callback
function, and the other method is directly calling the function with the decorators.

Basic Usage:
```python
import dash
from dash_callback_conglomerate import Router

app = dash.Dash(__name__)
router = Router(app, True)

@app.callback(Output('component', 'property'),
              Input('component', 'property'))
def callback(value):
    ...
    return 'value'

router.register_callbacks()

if __name__ == '__main__':
    app.run_server(debug=True)
```