# Python imports
import random
import string


def provide_authorization_credentials_to_client(client, access_token: str):
    """
    provides JWT authorization header
    """
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    return client


def generate_password(length):
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

    random.shuffle(characters)

    password = []

    for _ in range(length):
        password.append(random.choice(characters))

    ## shuffling the resultant password
    random.shuffle(password)

    ## converting the list to string
    ## printing the list
    return "".join(password)
