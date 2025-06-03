from django.utils import translation


class AdminLocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/'):
            user_language = request.COOKIES.get('django_language', 'en-us')
            translation.activate(user_language)
            request.LANGUAGE_CODE = translation.get_language()
        return self.get_response(request)
