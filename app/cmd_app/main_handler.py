""" main handler for the cmd_app """
import time

# from cmd_app.add_transaction import add_handler
# from cmd_app.view_transaction import view_handler
# from cmd_app.delete_transaction import delete_handler
# from cmd_app.record_payment import record_handler
# from cmd_app.view_balances import view_balances_handler
# from cmd_app.view_payments import view_payments_handler

from app.cmd_app.utils.api import handle_get_payload
# from cmd_app.utils.constants import PrintColor
# from cmd_app.utils.title_page import show_title
# from cmd_app.utils.file_io import copy_from_cloud, error_handler, push_to_cloud

OPTION_STATES = {
    "v": "view",
    "view": "view",
    "t": "view",
    "transaction": "view",
    "h": "history",
    "history": "history",
    "a": "add",
    "add": "add",
    "d": "delete",
    "delete": "delete",
    "s": "record",
    "settle": "record",
    "b": "balance",
    "balance": "balance",
    "e": "exit",
    "exit": "exit",
    "q": "exit",
    "quit": "quit"
}

def exit_handler(_: str) -> bool:
    """ Handles exiting the program """
    # print(f"\r\nWe'll start to {PrintColor.YELLOW}EXIT{PrintColor.NORMAL}...")
    print("\r\nExiting...")
    time.sleep(1)
    return False


ACTION_FUNCTIONS = {
    # "balance": view_balances_handler,
    # "view": view_handler,
    # "history": view_payments_handler,
    # "add": add_handler,
    # "delete": delete_handler,
    # "record": record_handler,
    "exit": exit_handler
}


def what_to_do_options():
    """ Prompts user to potential SplitWiser actions """
    matched = None
    while matched is None:
        options = "What would you like to do? Options include:\r\n\r\n"
        # options += f"\t- View {PrintColor.MAGENTA}BALANCES{PrintColor.NORMAL} between "
        # options += "accounts (b or balance)\r\n"
        # options += f"\t- View {PrintColor.CYAN}TRANSACTIONS{PrintColor.NORMAL} "
        # options += "(v or view, t or transaction)\r\n"
        # options += f"\t- View payment {PrintColor.HIGHLIGHT}HISTORY{PrintColor.NORMAL} "
        # options += "(h or history)\r\n"
        # options += f"\t- {PrintColor.GREEN}ADD{PrintColor.NORMAL} transactions (a or add)\r\n"
        # options += f"\t- {PrintColor.RED}DELETE{PrintColor.NORMAL} Transaction (d or delete)\r\n"
        # options += f"\t- {PrintColor.BLUE}SETTLE UP{PrintColor.NORMAL} / make a payment "
        # options += "(s or settle)\r\n"
        # options += f"\t- {PrintColor.YELLOW}EXIT{PrintColor.NORMAL} (e or exit, q or quit)"
        print(options)
        passed = input("\r\nSo... what would you like to do? ")
        passed = passed.lower().strip()
        matched = OPTION_STATES.get(passed)
        if not matched:
            print(f"\r\nI'm sorry, but '{passed}' is not a valid input. Please try again...\r\n")
            time.sleep(2)
    return matched

###################################################

def run(base_url: str):
    """run

    Runs the main command loop of options

    Args:
        base_url (str): api base url
    """
    is_running = True
    while is_running:
        action = what_to_do_options()
        is_running = ACTION_FUNCTIONS[action](base_url)


def boot_up_sync(pwd: str) -> bool:
    """boot_up_sync

    Boots up the app + copies the xlsx db file from the cloud

    Args:
        pwd (str): current working directory path

    Returns:
        bool: on success of copying xlsx db file from cloud location
    """
    # show_title()
    # is_successful = copy_from_cloud(pwd)
    # if not is_successful:
    #     error_handler("Missing path files. Exiting...")
    #     time.sleep(2)
    #     return False
    return True


def close_out_sync(pwd: str) -> bool:
    """cloud_out_sync

    Closes down the app + copies the xlsx db file to the cloud

    Args:
        pwd (str): current working directory path

    Returns:
        bool: on success of copying xlsx db file to cloud location
    """
    # is_successful = push_to_cloud(pwd)
    # if not is_successful:
    #     error_handler("Copying to cloud issue.")
    #     time.sleep(2)
    #     return False
    return True


def startup(base_url: str) -> None:
    """startup

    Boots up the api and DB portion, and continues to try hitting the API until it is ready

    Args:
        base_url (str): base url of the API
    """
    has_succeeded = False
    while not has_succeeded:
        try:
            handle_get_payload(f"{base_url}/start", skip_response=True)
            has_succeeded = True
        except: # pylint: disable=bare-except
            pass
        time.sleep(1)


def shutdown(base_url: str) -> None:
    """shutdown

    Shuts down the api (which saves the local DB to the xlsx db file)

    Args:
        base_url (str): base url of the API
    """
    print("\r\nShutting down...")
    handle_get_payload(f"{base_url}/shutdown", skip_response=True)
