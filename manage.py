from collaborator_app.controller import MainController
from initiate_table import initialize_database, create_admin_collaborator

initialize_database()
create_admin_collaborator()
MainController.run()
