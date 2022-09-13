# TODO: add update checker and auto-updater features
import urllib.request as urllib_request
import json

release_info = json.loads(urllib_request.urlopen(
        urllib_request.Request("https://api.github.com/repos/KJHJason/Cultured-Downloader/releases/latest"),
        timeout=10
    ).read().decode("utf-8"))