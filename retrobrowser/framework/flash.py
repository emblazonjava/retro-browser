class Flash(object):
    """
    An object for holding controller flash messages
    """

    error = '' # String for sending error messages to the user
    message = '' #String for sending messages to the user

    def render_error(self):
        """
        Render the Flash error from the controller
        :return:

        >>> flash = Flash()
        >>> flash.error = 'There is an error'
        >>> flash.message = 'A message for the user'
        >>> print (flash.render_error())
        <BLANKLINE>
        error: There is an error
        """

        output = ''
        if self.error != '':
            output = "\nerror: {0}".format(self.error)

        return output

    def render_message(self):
        """
        Render the Flash message from the controller
        :return:

        >>> flash = Flash()
        >>> flash.message = 'A message for the user'
        >>> print (flash.render_message())
        <BLANKLINE>
        A message for the user
        """

        output = ''
        if self.message != '':
            output = "\n{0}".format(self.message)

        return output

    def clear(self):
        """
        Clear the Flash error and message messages
        :return:

        >>> flash = Flash()
        >>> flash.error = 'There is an error'
        >>> flash.message = 'A message for the user'
        >>> print (flash.render_error())
        <BLANKLINE>
        error: There is an error
        >>> print (flash.render_message())
        <BLANKLINE>
        A message for the user
        >>> flash.clear()
        >>> print (flash.render_error())
        <BLANKLINE>
        >>> print (flash.render_message())
        <BLANKLINE>
        """

        self.error = ''
        self.message = ''
