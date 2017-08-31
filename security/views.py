from rest_framework import views
from rest_framework.response import Response


class PollAuthenticationView(views.APIView):
    """
    An empty view used to test authentication. Returns 401 status code if unauthorized.
    """
    def get(self, request):
        return Response({'status': 'authenticated'})
