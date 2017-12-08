import retrobrowser.framework.errors as errors

def parse_controller_and_action(input):
    """
    Parse the input String into controller and action names
    :param input: str input string
    :return:

    >>> (controller, action) = parse_controller_and_action('to main/index')
    >>> print (controller)
    main
    >>> print (action)
    index
    >>> (controller, action) = parse_controller_and_action('a main/index')
    >>> print (controller)
    None
    >>> print (action)
    None
    >>> (controller, action) = parse_controller_and_action('to main')
    >>> print (controller)
    main
    >>> print (action)
    index
    """

    controller_name = None
    action_name = None

    #if len(url) != 2:
    #    controller_name = None
    #    action_name = None
    url = input.split(' ')
    if len(url) == 2 and url[0] == 'to':
        parts = url[1].split('/')
        if len(parts) == 1:
            controller_name = parts[0].strip()
            action_name = 'index'
        elif len(parts) == 2:
            controller_name = parts[0]
            action_name = parts[1].strip().split('?')[0]
        else:
            controller_name = None
            action_name = None
    return (controller_name, action_name)

def parse_query_string(input, builder):
    """
    Parse the query string from the input
    :param input:
    :return:

    >>> import retrobrowser.framework.builder as b
    >>> builder = b.Builder()
    >>> print (parse_query_string('to gamePlay/submit?space=1', builder))
    {'space': '1'}
    >>> parse_query_string('to gamePlay/submit?space?', builder)
    {}
    >>> print (builder.package_name)
    <BLANKLINE>
    >>> print (builder.controller_name)
    error400
    >>> print (builder.action_name)
    index
    """

    url = input.split('?')
    params = {}
    if len(url) == 2:
        query_string = url[1].strip()
        pairs = query_string.split('&')
        for pair in pairs:
            pair_parts = pair.split('=')
            if len(pair_parts) == 2:
                (key, value) = pair_parts
                params[key] = value
            elif len(pair_parts) > 2:
                builder.handle_error(errors.ERROR_400)
            else:
                params[pair_parts[0]] = None
    elif len(url) > 2:
        builder.handle_error(errors.ERROR_400)

    return params

if __name__ == '__main__':
    import doctest
    doctest.testmod()