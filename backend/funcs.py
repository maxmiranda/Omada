"""Utility functions for Omada."""

import os

from api.omada_db_api import OmadaDB

def connect_db():

    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASS')

    if any([var is None for var in [db_user, db_pass]]):
        import config_vars

        db_user = config_vars.USER
        db_pass = config_vars.PASS

    mongo = OmadaDB({"user": db_user, "pass": db_pass})

    return mongo
