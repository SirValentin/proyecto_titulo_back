from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework.serializers import (
    CharField,
)
from planificador.models import User, Admin
from django.db import IntegrityError, transaction


class SignUpUserSerializer(BaseUserRegistrationSerializer):
    organization_name = CharField(required=False)

    class Meta(BaseUserRegistrationSerializer.Meta):
        model = User
        fields = ("organization_name",)

    # default_error_messages = {
    #     "empty_organization_name": "Organization Name is Required",
    #     "password_mismatch": djoser_settings.CONSTANTS.messages.PASSWORD_MISMATCH_ERROR,
    # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["re_password"] = CharField(style={"input_type": "password"})

    def validate(self, attrs):
        # self.fields.pop("re_password", None)
        # re_password = attrs.pop("re_password")
        # org_name = attrs.pop("organization_name")
        attrs = super().validate(attrs)

        # if attrs["password"] == re_password:
        #     if org_name:
        print(attrs)
        return attrs

    #     else:
    #         self.fail("empty_organization_name")
    # else:
    #     self.fail("password_mismatch")

    def create(self, validated_data):
        try:
            print(self)
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user

    def perform_create(self, validated_data):
        print(self)
        org_name = self.initial_data["organization_name"]
        # with transaction.atomic():
        # user = User.objects.create_admin_user(**validated_data)
        # if djoser_settings.SEND_ACTIVATION_EMAIL:
        #     user.is_verified = False
        #     user.save(update_fields=["is_verified"])

        # organization = Organization.objects.create(name=org_name, owner_id=user.id)
        # ClientOptions.objects.create(organization=organization)
        # rol, created = Roles.objects.get_or_create(
        #     name="Admin", organization=organization
        # )
        # admin = Admin.objects.create(
        #     related_user=user, organization=organization, role=rol
        # )
        # user.administradores.add(admin)
        # user.save()
        return user
