# Google OAuth2 Helper Program

**IMPORTANT**: This assumes that you have completed step 1 to 3 of the [Google OAuth2 Guide](google_oauth2_guide.md). Otherwise, follow the guide first before reading the rest of this guide.

When running [google_oauth.py](/src/helper/google_oauth.py), you will need the following flags:

- `-cp` or `--client-path`: Path to the client_secret.json file.
- `-s` or `--scopes`: Scopes to use for the Google OAuth2
  - Allowed Scopes: 
    - `https://www.googleapis.com/auth/drive.readonly`
  - Other scopes are not allowed and the main Cultured Downloader program will reject your generated token JSON file.
- `-tp` or `--token-path`: Path to save the generated token JSON file.
  - Recommended to follow the source code so that Cultured Downloader can detect the token file and handle with it.
    - Refer to the source code at [constants.py](https://github.com/KJHJason/Cultured-Downloader/blob/90e3b7ec892224a5723effda7a34920efe50e509/src/utils/constants.py#L34-L49) or refer to the path below:
      - Windows: `C:\Users\{username}\AppData\Roaming\Cultured-Downloader\google-oauth2-token.json`
      - Linux: `/home/{username}/.config/Cultured-Downloader/google-oauth2-token.jsonn`
      - macOS: `/Users/{username}/Library/Preferences/Cultured-Downloader/google-oauth2-token.json`
- `p` or `--port`: Port to use for the Google OAuth2 flow local server.
  - Defaults to port `8080` if not specified.