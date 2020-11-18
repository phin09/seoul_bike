import os
import json
from seoulbike.settings import BASE_DIR
from django.core.exceptions import ImproperlyConfigured

def get_secret(keyfile, setting):
    secret_file = os.path.join(BASE_DIR, keyfile)
    with open(secret_file) as f:
        secrets = json.loads(f.read())

    def secret_key(setting, secrets=secrets):
        try:
            #print("check: ", secrets[setting])
            return secrets[setting]
        except KeyError:
            error_msg = "Set the {} environment variable in secrets.json".format(setting)
            raise ImproperlyConfigured(error_msg)

    return secret_key(setting, secrets)