import dash.exceptions
from dash.dependencies import Input, Output, State
import logging


class PartialUpdate(Exception):
    def __init__(self, results):
        self.results = results


class Router(object):
    def __init__(self, app, hijack_callbacks=False, disable_all_verification=False):
        self.app = app
        self.callbacks = []

        if hijack_callbacks:
            setattr(app, 'original_callback', app.callback)
            setattr(app, 'callback', self.callback)

        if disable_all_verification:
            def validate(self, output, inputs, state):
                return True
            setattr(app, '_validate_callback', validate)

    def callback(self, outputs, inputs=[], states=[]):

        def wrap_func(func):
            self.callbacks.append({'func': func,
                                   'outputs': outputs if isinstance(outputs, list) else [outputs],
                                   'inputs': inputs if isinstance(inputs, list) else [inputs],
                                   'states': states if isinstance(states, list) else [states]})
            return func

        return wrap_func

    def register_callbacks(self):
        qualified_callbacks = []
        inputs = []
        outputs = []
        states = []
        for callback in self.callbacks:
            qualified_callback = {'inputs': [], 'parameters': [], 'results': [], 'func': callback['func']}
            for input in callback['inputs']:
                qualified_callback['inputs'].append(input.component_id + '.' + input.component_property)
                qualified_callback['parameters'].append(input.component_id + '.' + input.component_property)
                if State(input.component_id, input.component_property) in states:
                    states.pop(states.index(State(input.component_id, input.component_property)))
                if input not in inputs:
                    inputs.append(input)
            for state in callback['states']:
                qualified_callback['parameters'].append(state.component_id + '.' + state.component_property)
                # Todo: prevent multiple copies?
                if state not in states and Input(state.component_id, state.component_property) not in inputs:
                    states.append(state)
            for output in callback['outputs']:
                qualified_callback['results'].append(output.component_id + '.' + output.component_property)
                if output not in outputs:
                    outputs.append(output)
            qualified_callbacks.append(qualified_callback)

        callback_outputs = [output.component_id + '.' + output.component_property for output in outputs]

        parameters = [input.component_id + '.' + input.component_property for input in inputs]
        state_parameters = [state.component_id + '.' + state.component_property for state in states if
                            state.component_id + '.' + state.component_property not in parameters]
        parameters = parameters + state_parameters
        for output in callback_outputs:
            if output not in parameters:
                parameters.append(output)
                states.append(State(*output.split('.')))

        #print(inputs)
        #print(outputs)
        #print(states)
        #print(parameters)
        #print(callback_outputs)
        #print(qualified_callbacks)

        @self.app.original_callback(outputs, inputs, states)
        def _callbacks(*args):
            print(args)
            print(dash.callback_context.triggered)
            callback_results = []
            for output in callback_outputs:
                callback_results.append(args[parameters.index(output)])
            print('Previous states: {}'.format(callback_results))
            # Todo: Possibly sort by a priority parameter, if set, to delay call to after others with same input
            for qualified_callback in qualified_callbacks:
                for triggered in dash.callback_context.triggered:
                    if triggered['prop_id'] in qualified_callback['inputs']:
                        try:
                            results = qualified_callback['func'](
                                *[args[parameters.index(param)] for param in qualified_callback['parameters']])
                        except dash.exceptions.PreventUpdate:
                            break
                        # Todo: Possible support for integer indices for parameters for partial updates
                        except PartialUpdate as e:
                            for id, value in e.results.items():
                                if id not in callback_outputs:
                                    logging.warning('Can\'t output to \'{}\' because it hasn\'t been '
                                                    'registered in a callback decorator'.format(id))
                                    continue
                                callback_results[callback_outputs.index(id)] = value
                            break
                        if isinstance(results, (list, tuple)):
                            for i in range(len(results if isinstance(results, list) else list(results))):
                                callback_results[callback_outputs.index(qualified_callback['results'][i])] = results[i]
                        else:
                            callback_results[callback_outputs.index(qualified_callback['results'][0])] = results
                        break
            print('New states: {}'.format(callback_results))
            return callback_results
