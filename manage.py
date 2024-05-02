from collaborator_app.controller import MainController
from initiate_table import initialize_database, create_admin_collaborator, create_contract, create_event, create_client

initialize_database()
create_admin_collaborator()
create_client()
create_contract()
create_event()
MainController.run()
