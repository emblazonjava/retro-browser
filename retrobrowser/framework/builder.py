import importlib
import retrobrowser.framework.flash as flash
import retrobrowser.framework.errors as errors

class Builder(object):
    """
    Builder class for Controller objects, View objects, and action method objects
    """

    def __init__(self):
        self._controllers = ControllerDict()
        self.package_name = ''
        self.controller_name = ''
        self.action_name = ''
        self.params = {}

    def set_package_controller_and_action(self, package_name, controller_name, action_name):
        """
        Set the package, controller, and action names.
        If any of these are None, sets them all to the default 404 values.
        :param package_name:
        :param controller_name:
        :param action_name:
        :return:

        >>> builder = Builder()
        >>> builder.set_package_controller_and_action('tictactoe', 'gamePlay', 'submit')
        >>> print (builder.package_name)
        tictactoe
        >>> print (builder.controller_name)
        gamePlay
        >>> print (builder.action_name)
        submit
        """

        self.set_package_name(package_name)
        self.set_controller_name(controller_name)
        self.set_action_name(action_name)
        if (self.package_name == None) or (self.controller_name == None) or (self.action_name == None):
            self.handle_error(errors.ERROR_404)

    def set_package_name(self, package_name):
        """
        Set the package name
        :param package_name:
        :return:
        """

        self.package_name = package_name

    def set_controller_name(self, controller_name):
        """
        Set the controller name.
        :param controller_name:
        :return:
        """

        self.controller_name = controller_name

    def set_action_name(self, action_name):
        """
        Set the action name
        :param action_name:
        :return:
        """

        self.action_name = action_name

    def set_params(self, params):
        """
        Set the params Dictionary
        :param params:
        :return:
        """

        self.params = params

    def get_controller(self):
        """
        Instantiate a controller based on the package and controller names
        :return:
        """

        controller = None
        fully_qualified_controller_class_name = self._get_fully_qualified_controller_class_name()
        if self._controllers[fully_qualified_controller_class_name]:
            controller = self._controllers[fully_qualified_controller_class_name]
        else:
            controller_module = importlib.import_module(self._get_controller_module_name())

            controller = getattr(controller_module, self._get_controller_class_name())()

            # Inject self so that the builder action can be set by a call to redirect
            controller.builder = self
            # Inject the redirect method into the new controller
            controller.redirect = self._redirect
            # Set flash here to avoid having to call super() in child controller
            # only set it if it hasn't already been set, since controller is a singleton
            if not hasattr(controller, 'flash'):
                controller.flash = flash.Flash()

            # Implementing the singleton pattern for controller classes
            self._controllers[fully_qualified_controller_class_name] = controller

        # Set the params map
        controller.params = self.params

        return controller

    def _redirect(self, action):
        """
        This method is injected into the Controller sub-class objects. It enables one action
        to redirect to another. Currently only implemented for actions within the same
        Controller class
        :param action: The action to redirect to
        :return: The Dictionary returned from the redirect action
        """

        # Set this builder's action_name so that it will identify the rendered view
        self.set_action_name(action)
        # Get the action method object on the controller
        action_method_object = getattr(self.get_controller(), action)

        # call the redirect method and return it's Dictionary
        return action_method_object()

    def get_view(self, dict):
        """
        Instantiate a view based on the package, controller, and action names and the Dictionary
        from the controller action
        :param dict: A Dictionary of values from the Controller action to pass to the View
        :return:
        """

        view_module = importlib.import_module(self._get_view_module_name())

        return getattr(view_module, self._get_view_class_name())(dict)

    def get_action(self):
        """
        Get the action method object on this controller based on the package, controller, and action names
        :return:
        """
        return getattr(self.get_controller(), self._get_action_method_name())

    def _get_fully_qualified_controller_class_name(self):
        return self._get_controller_module_name() + '.' + self._get_controller_class_name()

    def _get_controller_module_name(self):
        """
        Get the controller module name based on the package and controller names
        :return:

        >>> builder = Builder()
        >>> builder.set_package_controller_and_action('tictactoe', 'gamePlay', 'play')
        >>> print (builder._get_controller_module_name())
        tictactoe.controllers.GamePlayController
        >>> builder.set_package_controller_and_action('', 'error404', 'index')
        >>> print (builder._get_controller_module_name())
        retrobrowser.framework.defaultapp.controllers.Error404Controller
        """

        package_name = ''
        if self.package_name != '':
            package_name = self.package_name
        else:
            package_name = 'retrobrowser.framework.defaultapp'

        return '{0}.controllers.{1}'.format(package_name,
                                            self._get_controller_class_name())

    def _get_view_module_name(self):
        """
        Get the view module name based on the package, controller, and action names
        :return:

        >>> builder = Builder()
        >>> builder.set_package_controller_and_action('tictactoe', 'gamePlay', 'play')
        >>> print (builder._get_view_module_name())
        tictactoe.views.GamePlay.PlayView
        >>> builder.set_package_controller_and_action('', 'error404', 'index')
        >>> print (builder._get_view_module_name())
        retrobrowser.framework.defaultapp.views.Error404.IndexView
        """

        package_name = ''
        if self.package_name != '':
            package_name = self.package_name
        else:
            package_name = 'retrobrowser.framework.defaultapp'

        return '{0}.views.{1}.{2}'.format(  package_name,
                                            self._get_view_package_name(),
                                            self._get_view_class_name()
                                           )

    def _get_controller_class_name(self):
        """
        Get the controller class name based on the package and controller names
        :return:

        >>> builder = Builder()
        >>> builder.set_package_controller_and_action('tictactoe', 'gamePlay', 'play')
        >>> print (builder._get_controller_class_name())
        GamePlayController
        >>> builder.set_package_controller_and_action('tictactoe', '', '')
        >>> print (builder._get_controller_class_name())
        None
        """

        controller_name_first_letter = ''
        controller_name_rest = ''
        if len(self.controller_name) == 0:
            return None
        else:
            controller_name_first_letter = self.controller_name[0].upper()
            if len(self.controller_name) > 1:
                controller_name_rest = self.controller_name[1:]

        return '{0}{1}Controller'.format(controller_name_first_letter, controller_name_rest)


    def _get_action_method_name(self):
        """
        Get the action method object name based on the package, controller, and action names
        :return:

        >>> builder = Builder()
        >>> builder.set_package_controller_and_action('tictactoe', 'gamePlay', 'newGame')
        >>> print (builder._get_action_method_name())
        new_game
        >>> builder.set_package_controller_and_action('tictactoe', 'gamePlay', '')
        >>> print (builder._get_action_method_name())
        <BLANKLINE>
        """

        action_method_name = ''
        if len(self.action_name) > 0:
            action_method_name = self.action_name[0].lower()
            if len(self.action_name) > 1:
                for char in self.action_name[1:]:
                    if char.isupper():
                        action_method_name += '_'
                    action_method_name += char.lower()

        return action_method_name

    def _get_view_package_name(self):
        """
        Get the view package name based on the package, controller, and action names
        :return:

        >>> builder = Builder()
        >>> builder.set_package_controller_and_action('tictactoe', 'gamePlay', 'play')
        >>> print (builder._get_view_package_name())
        GamePlay
        """

        controller_name_first_letter = ''
        controller_name_rest = ''
        if len(self.controller_name) == 0:
            return None
        else:
            controller_name_first_letter = self.controller_name[0].upper()
            if len(self.controller_name) > 1:
                controller_name_rest = self.controller_name[1:]

        return '{0}{1}'.format(controller_name_first_letter, controller_name_rest)


    def _get_view_class_name(self):
        """
        Get the view class name based on the package, controller, and action names
        :return:

        >>> builder = Builder()
        >>> builder.set_package_controller_and_action('tictactoe', 'gamePlay', 'play')
        >>> print (builder._get_view_class_name())
        PlayView
        """

        view_name_first_letter = ''
        view_name_rest = ''
        if len(self.action_name) == 0:
            return None
        else:
            view_name_first_letter = self.action_name[0].upper()
            if len(self.action_name) > 1:
                view_name_rest = self.action_name[1:]

        return '{0}{1}View'.format(view_name_first_letter, view_name_rest)

    def handle_error(self, error_number):
        """
        Set the package, controller, and action names to the ones corresponding to a 404 error
        :param error_number: The http error number
        :return:

        >>> builder = Builder()
        >>> builder.set_package_controller_and_action('tictactoe', 'gamePlay', 'play')
        >>> builder.handle_error('404')
        >>> print (builder.package_name)
        <BLANKLINE>
        >>> print (builder.controller_name)
        error404
        >>> print (builder.action_name)
        index
        """

        self.set_package_controller_and_action('', 'error' + error_number, 'index')


class ControllerDict(dict):
    def __missing__(self, key):
        return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()
