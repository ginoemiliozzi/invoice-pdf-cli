import pickle
import os
import utils
from typing import Generator
from models import Client

CLIENTS_PATH = '.clients.pkl'

def save_client(client: Client):
    with open(CLIENTS_PATH, 'ab') as file:
        pickle.dump(client, file)
        utils.success(f"Client {client.name} created")

def get_all_clients() -> Generator[Client, None, None]:
    if os.path.exists(CLIENTS_PATH):
        with open(CLIENTS_PATH, 'rb') as file:
            while True:
                try:
                    yield pickle.load(file)
                except EOFError:
                    break
    else:
        utils.warning("No clients found")
        yield from ()

def get_next_client_number():
    max_existing_number = max(
        list(map(lambda i: i.client_number, get_all_clients())),
        default=0
    )
    return max_existing_number + 1

def create_client() -> Client:
    client_number = get_next_client_number()
    client_name = utils.get_valid_input_type(str, "Enter the client business name:\n")
    client_address = utils.get_valid_input_type(str, "Enter the client address:\n")
    client_tax_id = utils.get_valid_input_type(str, "Enter the client tax id:\n")

    return Client(client_number, client_name, client_address, client_tax_id)

def get_client_by_number(number) -> Client | None:
    return next((client for client in get_all_clients() if client.client_number == number), None)

def choose_from_existing_clients() -> Client | None:
    utils.title("Select a client number")
    clients = list(get_all_clients())
    for client in clients:
        print(f"\n{client}")
    number = utils.get_valid_input_type(int, "Enter a client number: ")
    found = get_client_by_number(number)
    print(found)
    return found

