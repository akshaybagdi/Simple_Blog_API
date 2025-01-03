from rest_framework.authentication import TokenAuthentication

class QueryParamTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        if token:
            return self.authenticate_credentials(token)
        return super().authenticate(request)
