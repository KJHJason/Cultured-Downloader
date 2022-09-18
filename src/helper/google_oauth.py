# import Python's standard libraries
import json
import pathlib
from argparse import ArgumentParser

# import third-party libraries
from google_auth_oauthlib.flow import InstalledAppFlow

def save_google_oauth_json(json_data: str, file_path: str) -> None:
    """Saves the json data to a file"""
    with open(pathlib.Path(file_path), "w") as json_file:
        json_file.write(json_data)

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "-j",
        "--json",
        type=str,
        required=True,
        help="The client secret JSON value"
    )
    parser.add_argument(
        "-s",
        "--scopes",
        type=str,
        nargs="+",
        required=True,
        help="The scopes to use for the OAuth2 flow"
    )
    parser.add_argument(
        "-tp",
        "--token-path",
        type=str,
        required=True,
        help="The path to save the OAuth2 token"
    )
    args = vars(parser.parse_args())

    try:
        parsed_json = json.loads(args["json"])
    except (TypeError, json.JSONDecodeError):
        raise TypeError("client_json_value must be a valid json string")

    flow = InstalledAppFlow.from_client_config(parsed_json, args["scopes"])
    try:
        creds = flow.run_local_server(port=8080)
    except (KeyboardInterrupt):
        print("Cancelled by user.")
    else:
        save_google_oauth_json(
            json_data=creds.to_json(), file_path=args["token_path"]
        )

if (__name__ == "__main__"):
    main()