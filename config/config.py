from peewee import PostgresqlDatabase

SECRET_KEY = "gOtasuoyQJePkRnMg56HCWn1YFEtmy2gOUV9GGPGzI4Jds0VmymF6PwKFewlt6KS"

DATABASE_NAME = 'epic_event_crm_final'
DATABASE_USER = 'user_collaborator'
DATABASE_PASSWORD = 'r1a2i3n4'
DATABASE_HOST = 'localhost'

db = PostgresqlDatabase(DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST)
