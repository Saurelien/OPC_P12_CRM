from datetime import timedelta, datetime
from faker import Faker
from faker.generator import random
from client_app.model import Client
from collaborator_app.model import Collaborator
from contract_app.model import Contract
from event_app.model import Event

fake = Faker()


def generate_collaborator(**kwargs):
    username = kwargs.setdefault('username', fake.user_name())
    password = kwargs.setdefault('password', fake.password())
    first_name = kwargs.setdefault('first_name', fake.first_name())
    last_name = kwargs.setdefault('last_name', fake.last_name())
    role = kwargs.setdefault('role', 'C')
    collaborator = Collaborator(
        username=username,
        first_name=first_name,
        last_name=last_name,
        role=role
    )
    collaborator.set_password(password)
    collaborator.save()
    return collaborator


def generate_collaborator_data(role="C", **kwargs):
    """
    VERSION TEST génèrer un dictionnaire de données de collaborateur aléatoire via faker mais en retournant directement
     la donnée au lieu de définir des variables VERSION TEST.
    """
    return {
        "username": kwargs.get('username', fake.user_name()),
        "password": kwargs.get('password', fake.password()),
        "first_name": kwargs.get('first_name', fake.first_name()),
        "last_name": kwargs.get('last_name', fake.last_name()),
        "role": role
    }


def generate_client(collaborator=None, **kwargs):
    if not collaborator:
        collaborator = generate_collaborator()

    first_name = kwargs.get('first_name', fake.first_name())
    last_name = kwargs.get('last_name', fake.last_name())
    email = kwargs.get('email', fake.email())
    phone_number = kwargs.get('phone_number', fake.phone_number())
    commercial_assignee = collaborator
    client = Client.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        commercial_assignee=commercial_assignee
    )
    return client


def generate_contract_data(client=None, collaborator=None, **kwargs):
    if not client:
        client = generate_client(collaborator)

    if not collaborator:
        collaborator = generate_collaborator(role="C")

    kwargs.setdefault('total_amount', random.randint(100, 1000))
    kwargs.setdefault('remaining_amount', kwargs['total_amount'])

    contract = Contract.create(
        client=client,
        commercial_assignee=collaborator,
        **kwargs
    )
    return contract


def generate_event_data(contract=None, collaborator=None, client=None, **kwargs):
    if not contract:
        contract = generate_contract_data()

    if not collaborator:
        collaborator = generate_collaborator(role=Collaborator.SUPPORT)

    if not client:
        client = contract.client

    client_info = (
        f"Prénom: {client.first_name}\n"
        f"Nom: {client.last_name}\n"
        f"Email: {client.email}\n"
        f"Téléphone: {client.phone_number}"
    )

    kwargs.setdefault('client_info', client_info)
    kwargs.setdefault('event_date_start', datetime.now())
    kwargs.setdefault('event_date_end', kwargs['event_date_start'] + timedelta(hours=24))
    kwargs.setdefault('postal_address', fake.address())
    kwargs.setdefault('attendees', random.randint(10, 100))
    kwargs.setdefault('notes', fake.paragraph())

    event = Event.create(
        contract=contract,
        client=client,
        client_info=kwargs['client_info'],
        support_contact=collaborator,
        event_date_start=kwargs['event_date_start'],
        event_date_end=kwargs['event_date_end'],
        postal_address=kwargs['postal_address'],
        attendees=kwargs['attendees'],
        notes=kwargs['notes']
    )

    event.save()
    if not event.id:
        raise ValueError("L'événement n'a pas d'ID après la sauvegarde.")

    if event.support_contact is None:
        raise ValueError("Le support contact est None après la sauvegarde.")

    print(f"\nEvènement créé avec succès:"
          f"\nEvent ID: {event.id},"
          f"\nAdresse postale: {event.postal_address},"
          f"\nSupport Contact: {event.support_contact},"
          f"\nid: {event.support_contact.id}")
    return event


def delete_collaborator(role_to_delete="C"):
    """
    Fonction utilitaire pour créer un collaborateur, le supprimer, et vérifier la suppression.

    :param role_to_delete: Le rôle du collaborateur à supprimer. Par défaut, est "C" pour Commercial.
    :return: Un booléen indiquant si la suppression a réussi.
    """

    collaborator_to_delete = generate_collaborator(role=role_to_delete)

    try:
        collaborator_to_delete.delete_instance()
        Collaborator.get_by_id(collaborator_to_delete.id)
    except Collaborator.DoesNotExist:
        return True

    return False
