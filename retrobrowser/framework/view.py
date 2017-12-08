class View(object):
    """
    The abstract base class of all GSPs
    """

    def __init__(self, dict):
        """
        Inject the key/value pairs from dict as variables in this class
        :param dict: the key/value pairs to inject
        :return:

        >>> view = View({'hello': 'world'})
        >>> print (view.hello)
        world
        """
        for key in dict:
            setattr(self, key, dict[key])

    def get_content(self):
        """
        Substitutes variables into a format String to produce the output String

        The constructor will inject the variables using the MetaClass so that dynamic variable
        names can be used as in a Grails GSP.

        :return: str The formatted string

        >>> class ConcreteView(View):
        ...    def get_content(self):
        ...        return "{0} is the first variable\\n{1} is the second".format(self.first, self.second)
        >>> view = ConcreteView({'first': 'a', 'second': 'b'})
        >>> output = view.get_content()
        >>> print (output)
        a is the first variable
        b is the second
        """
        raise NotImplementedError('Need to implement getContent')



if __name__ == '__main__':
    import doctest
    doctest.testmod()


