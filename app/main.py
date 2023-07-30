import eel
import os
import threading
import time
import json
import sys
import aggr
from aggregation.AggregationFactory import AggregationFactory

DATA_CONFS = json.load(open("settings.json", "r", encoding="utf-8"))
OUTJSON_PATH = "output/out.json"
current_html = {
    "DetailAggregation": "",
    "FilebaseAggregation": "",
    "MonthlyAggregation": "",
}


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


eel.init(resource_path("web"))


def writeFile(filepath, jsonBody):
    dir_name = os.path.dirname(filepath)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(json.dumps(jsonBody, ensure_ascii=False))


def readFile(filepath):
    if not os.path.exists(filepath):
        return ""
    f = open(filepath, "r", encoding="utf-8")
    contents = f.read()
    f.close()
    return contents


@eel.expose
def get_current_html():
    return current_html


# This function will run in a separate thread
def watch_folder(folder_path):
    strategies = AggregationFactory.create_strategies()

    while True:
        outJson = aggr.analyzeTxt()

        outJsonStr = json.dumps(outJson, ensure_ascii=False)
        beforeJsonStr = readFile(OUTJSON_PATH)

        if outJsonStr == beforeJsonStr:
            time.sleep(1)
            continue

        writeFile(OUTJSON_PATH, outJson)

        for key, context in strategies.items():
            aggregated_data, html = context.execute(outJson)
            writeFile(f"output/{key}.json", aggregated_data)
            writeFile(f"output/{key}.html", html)
            current_html[key] = html
            getattr(eel, key)(html)  # Function name and key name are identical

        time.sleep(1)


if os.path.exists(OUTJSON_PATH):
    os.remove(OUTJSON_PATH)

# Start the watcher thread
threading.Thread(target=watch_folder, args=(os.path.join(os.getcwd(), "input"),), daemon=True).start()

# Start the app
eel.start("index.html")
