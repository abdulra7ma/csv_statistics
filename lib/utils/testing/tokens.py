# Django imports
from django.urls import reverse


def get_tokens(client, cred={}):
    """
    gets access and refresh tokens
    """
    token_url = reverse("token_obtain_pair")
    tokens = client.post(token_url, data=cred)
    return tokens.data
