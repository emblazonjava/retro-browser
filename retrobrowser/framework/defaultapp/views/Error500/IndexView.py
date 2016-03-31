import retrobrowser.framework.view as view

class IndexView(view.View):
    """
    View to render a 500 error
    """

    def get_content(self):
        return '500 Server error. There was an internal error in the application.'


