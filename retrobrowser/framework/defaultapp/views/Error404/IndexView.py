import retrobrowser.framework.view as view

class IndexView(view.View):
    """
    View to render a 404 error
    """

    def get_content(self):
        return '404 Resource not found. RetroBrowser could not find the requested resource.'
