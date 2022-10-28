from validator_collection import checkers, errors
import graphene
# from graphene_file_upload.scalars import Upload

class ImageUploadInput(graphene.InputObjectType):
    # file = Upload()
    base64 = graphene.String()
    type = graphene.String()

class SocialSignInInput(graphene.InputObjectType):
    email = graphene.String()
    username = graphene.String()
    password = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()

    @staticmethod
    def validate_email(email, info, **input):
        is_email_address = checkers.is_email(email)
        if not is_email_address:
            raise errors.InvalidEmailError("Invalid email address")
        return email

    @staticmethod
    def validate_username(username, info, **input):
        is_email_address = checkers.is_email(username)
        if not is_email_address:
            raise errors.NotReadableError("Username wasn't valid")
        return username

    @staticmethod
    def validate_password(password, info, **input):
        if password == "":
            raise errors.EmptyValueError("Password required")
        if len(password) < 5:
            raise errors.MinimumLengthError("Password must be least 5 charactors")
        return password

class SendPasswordResetEmailInput(graphene.InputObjectType):
    email = graphene.String()

    @staticmethod
    def validate_email(email, info, **input):
        is_email_address = checkers.is_email(email)
        if not is_email_address:
            raise errors.InvalidEmailError("Invalid email address")
        return email
