from peewee import PostgresqlDatabase

DATABASE_NAME = 'nom_de_la_base_de_donnees'
DATABASE_USER = 'votre_utilisateur'
DATABASE_PASSWORD = 'votre_mot_de_passe'
DATABASE_HOST = 'localhost'

db = PostgresqlDatabase(DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST)