This is a Plotly Dash add-on for enabling more freedom with callback handling, enabling sharing inputs, outputs, and
only returning some of the outputs registered for a callback. There are two ways to use this add-on. One method is
seamless integration where the dash callback function is hijacked and replaced with a call to this modules callback
function, and the other method is directly calling the function with the decorators. Look at github for examples.