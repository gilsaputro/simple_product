import os
import sys
import json
import requests

def main():
    if len(sys.argv) < 2:
        print("ERROR: schema directory not supplied")
        sys.exit(1)

    dir_path = sys.argv[1]
    vault_host = os.environ.get("VAULT_HOST", "http://127.0.0.1:8200/v1/secret/data/")

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if not file.endswith(".json"):
                continue

            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                try:
                    value = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"ERROR: JSON decode error in file {file_path}: {e}")
                    continue

            filename = os.path.splitext(file)[0]
            url = f"{vault_host}{filename}"
            headers = {
                "content-type": "application/json",
                "X-Vault-Token": "root"  # You may need to replace this with the actual token
            }

            try:
                response = requests.post(url, json=value, headers=headers)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"ERROR: Failed to store secret based on schema {file_path}: {e}")
                continue

            if response.status_code != 200:
                print(f"ERROR: Failed to store secret based on schema {file_path}: code={response.status_code} resp={response.text}")
                continue

            print(f"INFO: Secret for file {filename} is created!")

if __name__ == "__main__":
    main()
