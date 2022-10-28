from django.core.signing import BadSignature, SignatureExpired
from django.shortcuts import render
from graphql_auth import exceptions, models

from .models import ExtendUser
from .schema.subscriptions import UserConfirm


def activation_view(request, id, token):
    try:
        models.UserStatus.verify(token)
        user = ExtendUser.objects.get(pk=id)
        UserConfirm.broadcast(
            # Subscription group to notify clients in.
            group=user.email,
            # Dict delivered to the `publish` method.
            payload=True,
        )
        return render(request, "confirmation/success.html")
    except exceptions.UserAlreadyVerified:
        return render(request, "confirmation/already_verified.html")
        # return cls(success=False, errors=constants.Messages.ALREADY_VERIFIED)
    except SignatureExpired:
        # return cls(success=False, errors=constants.Messages.EXPIRED_TOKEN)
        return render(request, "confirmation/expired.html")
    except (BadSignature, exceptions.TokenScopeError):
        # return cls(success=False, errors=constants.Messages.INVALID_TOKEN)
        return render(request, "confirmation/invalid_token.html")

    
    
