import retrobrowser.framework.view as view

class IndexView(view.View):
    """
    View to render a 400 error
    """

    def get_content(self):
        return '400 Bad Request. RetroBrowser cannot understand this request because it is poorly formed.'

