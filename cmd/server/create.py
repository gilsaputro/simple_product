import os
from flask import Flask
from cmd.config.load import get_config
from pkg.postgres.client import Database
from pkg.vault.client import VaultClient
from datetime import datetime
from dotenv import load_dotenv
from internal.repository.product.product_repository import ProductRepository
from internal.usecase.product.product_usecase import ProductUseCase
from internal.controller.product.product_controller import ProductController


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
    db = Database(cfg.Postgres.Config)
    loader("Init Database Connection Completed")
    
     # Init Repository
    loader("Init Repository Started")
    product_repository = ProductRepository(db)
    loader("Init Repository Completed")
    
    # Init Usecase
    loader("Init Usecase Started")
    product_usecase = ProductUseCase(product_repository)
    loader("Init Usecase Completed")
    
    # Init Usecase
    loader("Init Controller Started")
    product_controller = ProductController(product_usecase)
    loader("Init Controller Completed")
    
    app = Flask(__name__)
    app = product_controller.define_routes(app)

    return app

def loader(name):
    print(f'[Loader|{name}|{datetime.now()}]')