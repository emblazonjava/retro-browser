import sys
import retrobrowser.framework.builder as builder
import retrobrowser.framework.inputparser as inputparser
import retrobrowser.framework.errors as errors


class RetroBrowser(object):
    """
    The main framework class
    """

    def __init__(self):
        self.builder = builder.Builder()

    def main_loop(self, package_name):
        """
        The main loop of the RetroBrowser framework
        :param package_name: The package name of the RetroBrowser app to run
        :return:
        """

        controller_name = 'main'
        action_name = 'index'
        self.builder.set_package_controller_and_action(package_name, controller_name, action_name)
        self.builder.set_params({})
        self._instantiate_call_and_render()

        exit = False
        while not exit:
            print ('at {0}/{1}/{2}'.format(self.builder.package_name,
                                           self.builder.controller_name,
                                           self.builder.action_name
            ))
            print ('Input: '),
            # read input
            input = sys.stdin.readline()
            # parse location
            (controller_name, action_name) = inputparser.parse_controller_and_action(input)
            self.builder.set_package_controller_and_action(package_name, controller_name, action_name)
            params = inputparser.parse_query_string(input, self.builder)
            self.builder.set_params(params)
            # parse query string, if any

            self._instantiate_call_and_render()
            # else parse input as control of current page


    def _instantiate_call_and_render(self):
        """
        Instantiate the controller, call the action, and render the results
        :return:
        """

        try:
            action_method_object = self.builder.get_action()
        except ImportError as err:
            print ('ERROR: ImportError in RetroBrowser._instantiate_call_and_render: ' + str(err))
            self.builder.handle_error(errors.ERROR_404)
            action_method_object = self.builder.get_action()
        except AttributeError as err:
            print ('ERROR: AttributeError in RetroBrowser._instantiate_call_and_render: ' + str(err))
            self.builder.handle_error(errors.ERROR_404)
            action_method_object = self.builder.get_action()

        dict = {}
        try:
            dict = action_method_object()
        except Exception as err:
            print ('ERROR: Exception in the RetroBrowser app when calling action: ' + str(err))
            self.builder.handle_error(errors.ERROR_500)
            dict = self.builder.get_action()()

        # render the output string
        output = self._render(dict)

        # print to console
        print (output)

    def _render(self, dict):
        """
        Inject the Dictionary of key/value pairs into the View associated with controller.action
        to build the String to be output to the console

        :param dict: key/value pairs to inject into the View
        :return: str String to be output to the console
        """

        view = None
        controller = None
        try:
            view = self.builder.get_view(dict)
            controller = self.builder.get_controller()
        except ImportError as err:
            print ('ERROR: ImportError in RetroBrowser._render: ' + str(err))
            self.builder.handle_error(errors.ERROR_404)
            view = self.builder.get_view({})
            controller = self.builder.get_controller()
        except AttributeError as err:
            print ('ERROR: AttributeError in RetroBrowser._render: ' + str(err))
            self.builder.handle_error(errors.ERROR_404)
            view = self.builder.get_view({})
            controller = self.builder.get_controller()

        output = view.get_content()
        output += controller.flash.render_error()
        output += controller.flash.render_message()

        # Clear the flash and message messages
        controller.flash.clear()

        return output


if __name__ == '__main__':
    import doctest
    import importlib
    doctest.testmod()
    doctest.testmod(importlib.import_module('builder'))
    doctest.testmod(importlib.import_module('flash'))
    doctest.testmod(importlib.import_module('inputparser'))
    doctest.testmod(importlib.import_module('view'))
