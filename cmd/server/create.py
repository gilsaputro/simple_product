import os
from flask import Flask
from cmd.config.load import get_config
from pkg.postgres.client import Database
from pkg.vault.client import VaultClient
from datetime import datetime
from dotenv import load_dotenv

def create_server():
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve values from environment variables
    vault_token = os.getenv("VAULT_TOKEN")
    vault_address = os.getenv("VAULT_HOST")

    
    # Load Config
    loader("Init Vault Connection Started")
    vault = VaultClient(vault_token, vault_address)
    secret_values = vault.get_config()
    if not secret_values:
        print(f"Failed init vault")
        return
    
    cfg = get_config(secret_values)
    loader("Init Vault Completed")
    
    # Init Database
    loader("Init Database Connection Started")
    print(cfg.Postgres.Config)
    _ = Database(cfg.Postgres.Config)
    loader("Init Database Connection Completed")
    
    app = Flask(__name__)

    return app

def loader(name):
    print(f'[Loader|{name}|{datetime.now()}]')