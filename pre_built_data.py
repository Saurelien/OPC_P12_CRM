import peewee
from collaborator_app.model import Collaborator
from contract_app.model import Contract
from client_app.model import Client
from event_app.model import Event
import datetime


def create_admin_collaborator():
    if not Collaborator.select().where(Collaborator.username == 'admin').exists():
        print("Le collaborateur n'existe pas. Création en cours...")
        predefined_data = {
            "username": "admin",
            "password": "admin123",
            "first_name": "admin",
            "last_name": "admin",
            "role": Collaborator.GESTION
        }

        primary_collaborator = Collaborator(
            username=predefined_data["username"],
            first_name=predefined_data["first_name"],
            last_name=predefined_data["last_name"],
            role=predefined_data["role"]
        )
        primary_collaborator.set_password(predefined_data["password"])
        primary_collaborator.save()

        print("Collaborateur 'admin' créé avec succès.")
    else:
        print("Le collaborateur 'admin' existe déjà dans la base de données. Ignorant la création.")


def create_client():
    if not Collaborator.select().where(Collaborator.username == 'commercial_test').exists():
        print("Aucun client trouvé. Création en cours...")
        commercial_collaborator = Collaborator(
            username="commercial_test",
            first_name="Commercial",
            last_name="Test",
            role=Collaborator.COMMERCIAL
        )
        commercial_collaborator.set_password("password123")
        commercial_collaborator.save()

        predefined_data = {
            "first_name": "Gerard",
            "last_name": "Gniome",
            "email": "Gerard.Gniome@example.com",
            "phone_number": "123456789",
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "commercial_assignee": commercial_collaborator
        }

        client = Client(
            first_name=predefined_data["first_name"],
            last_name=predefined_data["last_name"],
            email=predefined_data["email"],
            phone_number=predefined_data["phone_number"],
            created_at=predefined_data["created_at"],
            updated_at=predefined_data["updated_at"],
            commercial_assignee=predefined_data["commercial_assignee"]
        )
        client.save()

        try:
            client.save()
        except peewee.IntegrityError as e:
            print(e)


def create_contract():
    if not Contract.select().where(Contract.id == '1').exists():
        print("Aucun contrat trouvé. Création en cours...")
        predefined_data = {
            "client": Client.get_or_create(first_name="Gerard", last_name="Gniome")[0],
            "total_amount": 1000,
            "remaining_amount": 1000,
            "created_date": datetime.date.today(),
            "updated_at": datetime.datetime.now(),
            "is_signed": False,
            "commercial_assignee": Collaborator.get_or_create(username="commercial_test")[0]
        }
        contract = Contract(
            client=predefined_data["client"],
            total_amount=predefined_data["total_amount"],
            remaining_amount=predefined_data["remaining_amount"],
            created_at=predefined_data["created_date"],
            updated_at=predefined_data["updated_at"],
            is_signed=predefined_data["is_signed"],
            commercial_assignee=predefined_data["commercial_assignee"]
        )
        contract.save()
        try:
            contract.save()
        except peewee.IntegrityError as e:
            print(e)


def create_event():
    if not Event.select().where(Event.id == '1').exists():
        support_collaborator = Collaborator(
            username="admin_support",
            first_name="support",
            last_name="test",
            role=Collaborator.SUPPORT
        )
        support_collaborator.set_password("password123")
        support_collaborator.save()
        print("Aucun événement trouvé. Création en cours...")
        predefined_data = {
            "contract": Contract.get_or_create(total_amount=1000)[0],
            "client": Client.get_or_create(first_name="Gerard", last_name="Gniome")[0],
            "support_contact": Collaborator.get_or_create(username="admin_support")[0],
            "event_date_start": datetime.datetime.now(),
            "event_date_end": datetime.datetime.now() + datetime.timedelta(hours=24),
            "postal_address": "21 jump street",
            "attendees": 10,
            "notes": "Lorem ipsum dolor sit amet, in vino veritas"
        }
        client_info = (f"First name: {predefined_data['client'].first_name}\n"
                       f"Last name: {predefined_data['client'].last_name}"
                       f"Email: {predefined_data['client'].email}\n"
                       f"Phone number: {predefined_data['client'].phone_number}")

        event = Event(
            contract=predefined_data["contract"],
            client=predefined_data["client"],
            client_info=client_info,
            support_contact=predefined_data["support_contact"],
            event_date_start=predefined_data["event_date_start"],
            event_date_end=predefined_data["event_date_end"],
            postal_address=predefined_data["postal_address"],
            attendees=predefined_data["attendees"],
            notes=predefined_data["notes"]
        )
        event.save()
        try:
            event.save()
        except peewee.IntegrityError as e:
            print(e)
