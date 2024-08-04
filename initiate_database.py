from peewee import PostgresqlDatabase, ProgrammingError

import config.config
from config.config import (ADMIN_USER, DATABASE_NAME,
                           DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD)
from config.config import db
from pre_built_data import create_admin_collaborator, create_client, create_contract, create_event
from initiate_table import initialize_database


def create_database():
    try:
        db_admin = PostgresqlDatabase('postgres', user=ADMIN_USER,
                                      password=DATABASE_PASSWORD,
                                      host=DATABASE_HOST)
    except Exception as e:
        print(f"Erreur lors de la connexion à la base de données 'postgres' : {e}")
        return

    try:
        db_admin.connect()
        print("Connexion réussie à PostgreSQL en tant qu'utilisateur 'postgres'.")
    except ProgrammingError as e:
        print(f"Erreur lors de la connexion à PostgreSQL : {e}")
        db_admin.close()
        return

    try:
        db_exists = db_admin.execute_sql(f"SELECT 1 FROM pg_database WHERE datname = '{DATABASE_NAME}'").fetchone()
    except ProgrammingError as e:
        print(f"Erreur lors de la vérification de l'existence de la base de données de test : {e}")
        db_admin.close()
        return

    if not db_exists:
        try:
            db_admin.execute_sql(f'CREATE DATABASE {DATABASE_NAME}')
            print(f"La base de données '{DATABASE_NAME}' a été créée avec succès.")
        except ProgrammingError as e:
            print(f"Erreur lors de la création de la base de données de test : {e}")
            db_admin.close()
            return
    else:
        print(f"La base de données '{DATABASE_NAME}' existe déjà.")

    db_admin.close()

    try:
        db_postgres = PostgresqlDatabase(DATABASE_NAME, user=ADMIN_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST)
        db_postgres.connect()
        print(f"Connexion réussie à la base de données '{DATABASE_NAME}' en tant qu'utilisateur '{ADMIN_USER}'.")
    except ProgrammingError as e:
        print(f"Erreur lors de la connexion à la base de données de test : {e}")
        return

    try:
        db_postgres.execute_sql(f"ALTER SCHEMA public OWNER TO {ADMIN_USER};")
        print("Le propriétaire du schéma public a été modifié en 'postgres'.")
    except ProgrammingError as e:
        print(f"Erreur lors de la modification du propriétaire du schéma public : {e}")
        db_postgres.close()
        return

    try:
        db_postgres.execute_sql(f"GRANT CREATE ON SCHEMA public TO {DATABASE_USER};")
        print(f"Autorisation de création accordée à l'utilisateur {DATABASE_USER} pour le schéma public.")
    except ProgrammingError as e:
        print(f"Erreur lors de l'attribution des autorisations : {e}")
        db_postgres.close()
        return

    try:
        # import ipdb
        # ipdb.set_trace()
        initialize_database()
        if config.config.ENVIRONMENT == "LOCAL":
            create_admin_collaborator()
            create_client()
            create_contract()
            create_event()

    except ProgrammingError as e:
        print(f"Erreur lors de la création des tables & données préconstruites dans '{DATABASE_NAME}': {e}")
    finally:
        db.close()
