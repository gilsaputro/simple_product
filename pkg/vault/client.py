import hvac

SECRET_PATH = "config"

class VaultClient:
    def __init__(self, token, address):
        if not token:
            raise ValueError("Error: Vault Token is invalid")

        self.client = hvac.Client(
            url=address,
            token=token,
        )
    def get_config(self):
        try:
            response = self.client.secrets.kv.read_secret_version(path=SECRET_PATH)
            data = response["data"]["data"]
            secret_map = {key: str(value) for key, value in data.items()}
            return secret_map
        except hvac.exceptions.VaultError as e:
            print(f"Error reading secret from Vault: {e}")
            return None