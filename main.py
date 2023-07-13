import eel
import os
import threading
import time
import json
import sys
import aggr
import conv

DATA_CONFS = json.load(open('settings.json', 'r', encoding='utf-8'))

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
eel.init(resource_path('web'))

def writeFile(outPath, jsonBody):
    f = open(outPath, 'w', encoding="utf-8")
    f.write(json.dumps(jsonBody, ensure_ascii=False))

# This function will run in a separate thread
def watch_folder(folder_path):
    while True:
        outJson = aggr.analyzeTxt()
        writeFile('out.json', outJson)
        outHtml = conv.json_to_html(outJson)
        eel.updateHTML(outHtml)  # Update the HTML content in the browser
        time.sleep(1)  # sleep for 1 second

# Start the watcher thread
threading.Thread(target=watch_folder, args=(os.path.join(os.getcwd(), 'input'),), daemon=True).start()

# Start the app
eel.start('index.html')
