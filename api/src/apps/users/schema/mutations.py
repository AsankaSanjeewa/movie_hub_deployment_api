import base64
import graphene
from smtplib import SMTPException
from django.contrib.auth import hashers
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.utils.module_loading import import_string
from graphene_validator.decorators import validated
from graphql_auth import (constants, exceptions, models, mutations, settings,
                          shortcuts, types, utils)
from graphql_jwt.decorators import login_required

from ..forms import EmailForm
from ..inputs import (ImageUploadInput, SendPasswordResetEmailInput,
                      SocialSignInInput)
from ..models import ExtendUser
from ..types import ImageUploadType
from ..tasks import send_password_reset_mail

if settings.graphql_auth_settings.CUSTOM_ERROR_TYPE and isinstance(settings.graphql_auth_settings.CUSTOM_ERROR_TYPE,
                                                                   str):
    OutputErrorType = import_string(
        settings.graphql_auth_settings.CUSTOM_ERROR_TYPE)
else:
    OutputErrorType = types.ExpectedErrorType

if settings.graphql_auth_settings.EMAIL_ASYNC_TASK and isinstance(settings.graphql_auth_settings.EMAIL_ASYNC_TASK, str):
    async_email_func = import_string(
        settings.graphql_auth_settings.EMAIL_ASYNC_TASK)
else:
    async_email_func = None


class ImageUpload(graphene.Mutation):
    class Arguments:
        imageInput = ImageUploadInput(required=True)

    image = graphene.Field(ImageUploadType)

    @staticmethod
    def mutate(root, info, imageInput=None):
        # format, imgstr = imageInput.base64.split(';base64,')
        # ext = format.split('/')[-1]
        ext = "png"
        data = ContentFile(base64.b64decode(
            imageInput.base64), name='temp.' + ext)

        user = ExtendUser.objects.get(id=info.context.user.id)
        if user:
            user.imageUrl.delete(save=True)
            # user.imageUrl = None
            user.save()

        user = ExtendUser.objects.get(id=info.context.user.id)
        if user:
            user.imageUrl = data
            user.save()

        return ImageUpload(image=user)


@validated
class SocialSignIn(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        inputs = SocialSignInInput(required=True)

    @staticmethod
    def mutate(root, info, inputs=None):
        try:
            user = ExtendUser.objects.filter(email=inputs.email)
            if user:
                raise Exception("Email address already exists")

            hashedPassword = hashers.make_password(inputs.password)

            user = ExtendUser(
                email=inputs.email,
                username=inputs.username,
                password=hashedPassword,
                first_name=inputs.firstName,
                last_name=inputs.lastName,
            )
            user.save()

            status = models.UserStatus.objects.get(user_id=user.id)
            if status:
                status.verified = True
                status.save()

            return SocialSignIn(message="Registration successfully", success=True)

        except Exception as e:
            print('SocialSignIn Exception:' + str(e))
            return SocialSignIn(message="Registration was Failed", success=False)


class SendPasswordResetEmail(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.Field(OutputErrorType)

    class Arguments:
        inputs = SendPasswordResetEmailInput(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        inputs = kwargs.get("inputs")
        try:
            f = EmailForm({"email": inputs.email})
            if f.is_valid():
                user = shortcuts.get_user_by_email(inputs.email)

                # Generate token
                token = utils.get_token(
                    user,
                    constants.TokenAction.PASSWORD_RESET
                )
                # run send mail task with celery
                send_password_reset_mail.delay(inputs.email, token)
                return cls(success=True)
            return cls(success=False, errors=f.errors.get_json_data())
        except ObjectDoesNotExist:
            return cls(success=True)  # even if user is not registered
        except SMTPException:
            return cls(success=False, errors=constants.Messages.EMAIL_FAIL)
        except exceptions.UserNotVerified:
            user = shortcuts.get_user_by_email(inputs.email)
            try:
                if async_email_func:
                    async_email_func(
                        user.status.resend_activation_email, (info,))
                else:
                    user.status.resend_activation_email(info)
                return cls(
                    success=False,
                    errors={
                        "email": constants.Messages.NOT_VERIFIED_PASSWORD_RESET},
                )
            except SMTPException:
                return cls(success=False, errors=constants.Messages.EMAIL_FAIL)


class Mutation:
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
    refresh_token = mutations.RefreshToken.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    # send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    send_password_reset_email = SendPasswordResetEmail.Field()
    reset_password = mutations.PasswordReset.Field()
    image_upload = ImageUpload.Field()
    social_sign_in = SocialSignIn.Field()
