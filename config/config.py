from peewee import PostgresqlDatabase

DATABASE_NAME = 'new_epic_event_crom_db'
DATABASE_USER = 'user_collaborator'
DATABASE_PASSWORD = 'r1a2i3n4'
DATABASE_HOST = 'localhost'

db = PostgresqlDatabase(DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST)
