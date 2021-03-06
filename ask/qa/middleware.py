from qa.models import Session
from django.utils import timezone

class CheckSessionMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            session_id = request.COOKIES.get('sessionid')
            session = Session.objects.get(
                    key=session_id,
                    expires__gt=timezone.now(),
                )
            request.session = session
            request.user = session.user
        except Session.DoesNotExist:
            request.session = None
            request.user = None
        return self.get_response(request)