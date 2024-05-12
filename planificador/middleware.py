from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import InvalidToken


class EmpresaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # TODO: implement
        # activate for admin

        # header_token = request.META.get("HTTP_AUTHORIZATION", None)
        # print(header_token)
        # print(request.user)
        # user = request.user
        # if user.is_authenticated:
        #     print(user)
        # if header_token is not None:
        #     try:
        #         user = authentication.JWTAuthentication().authenticate(
        #             request
        #         )  # Manually authenticate the token
        #         print(user)
        #         if user:
        #             request.user = user[0]
        #     except InvalidToken as e:
        #         pass

        # empresa_user = None
        # try:
        #     if request.user.selected_organization is not None:
        #         user_organization = request.user.selected_organization
        #     elif request.user.administradores.count() == 1:
        #         user_organization = request.user.administradores.first().organization
        #     elif request.user.colaboradores.count() == 1:
        #         user_organization = request.user.colaboradores.first().organization
        #     else:
        #         user_organization = None
        # except:
        #     user_organization = None

        # user_admin = None
        # try:
        #     user_admin = (
        #         Admin.objects.filter(user=request.user, organization=user_organization).first()
        #         if not request.user.is_anonymous
        #         else None
        #     )
        # except:
        #     user_admin = None

        # request.organization = user_organization
        # request.admin = user_admin

        response = self.get_response(request)
        return response
