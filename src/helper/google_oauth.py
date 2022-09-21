# import Python's standard libraries
import json
from argparse import ArgumentParser

# import third-party libraries
from google_auth_oauthlib.flow import InstalledAppFlow

if (__name__ == "__main__"):
    parser = ArgumentParser()
    parser.add_argument(
        "-cp",
        "--client-path",
        type=str,
        required=True,
        help="The client secret JSON file path",
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
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8080,
        help="The port to use for the OAuth2 flow"
    )
    args = vars(parser.parse_args())

    with open(args["client_path"], "r") as f:
        client_json_data = json.load(f)

    flow = InstalledAppFlow.from_client_config(
        client_config=client_json_data,
        scopes=args["scopes"]
    )
    creds = flow.run_local_server(port=args["port"])
    with open(args["token_path"], "w") as json_file:
        json_file.write(creds.to_json())