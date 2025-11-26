""" api utilities for cmd_app """
from typing import Union
import requests


def handle_get_payload(url: str, skip_response: bool = False) -> dict:
    """handle_get_payload

    Runs the requests for gets. 'skip_response' can be used for "command" gets, like 'startup' or
    'shutdown'

    Args:
        url (str): url of the request and route
        skip_response (bool, optional): to skip any meaningful return. Defaults to False.

    Returns:
        dict: dict/json response of the data (empty dict if error or 'skip_response')
    """
    data = requests.get(url, timeout=3)
    if data.status_code == 200 and not skip_response:
        return data.json()
    return {}


def handle_delete_id(url: str) -> Union[dict, None]:
    """handle_delete_id

    Runs the delete of an object by id (which should be included in the url)

    Args:
        url (str): url of the route with the ID to delete

    Returns:
        Union[dict, None]: returns the object if successful, else None on a failure
    """
    response = requests.delete(url, timeout=3)
    if response.status_code != 201:
        return None
    return response.json()


def handle_post(url: str, json_data: dict) -> None:
    """handle_post

    Runs any posting to the api of data

    Args:
        url (str): route to post to
        json_data (dict): json data to post
    """
    response = requests.post(url, json=json_data, timeout=3)
    if response.status_code != 201:
        print(f"ERROR on saving post to '{url}'. Response was: {response.status_code}")
