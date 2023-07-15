import eel
import os
import threading
import time
import json
import sys
import aggr
import conv

DATA_CONFS = json.load(open('settings.json', 'r', encoding='utf-8'))
OUTJSON_PATH = "output/out.json"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
eel.init(resource_path('web'))

def writeFile(filepath, jsonBody):
    dir_name = os.path.dirname(filepath)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(jsonBody, ensure_ascii=False))

def readFile(filepath):
    if not os.path.exists(filepath): return ""
    f =  open(filepath, 'r', encoding='utf-8') 
    contents = f.read()
    f.close()
    return contents
    
# This function will run in a separate thread
def watch_folder(folder_path):
    while True:
        outJson = aggr.analyzeTxt()

        outJsonStr = json.dumps(outJson, ensure_ascii=False)
        beforeJsonStr = readFile(OUTJSON_PATH)
        
        if outJsonStr == beforeJsonStr: 
            time.sleep(1)
            continue

        writeFile(OUTJSON_PATH, outJson)
        
        detail_html = conv.json_to_html(outJson)
        writeFile("output/detail.html", detail_html)
        eel.updateDetailHTML(detail_html)  

        # Generate the filebase aggregated HTML
        filebase_aggregated_data = conv.filebase_aggregate_data(outJson)
        filebase_aggregated_html = conv.json_to_html_aggregated(filebase_aggregated_data)
        writeFile("output/filebase_aggregated.html", filebase_aggregated_html)
        eel.updateFilebaseAggregatedHTML(filebase_aggregated_html)

        time.sleep(1)

if os.path.exists(OUTJSON_PATH): os.remove(OUTJSON_PATH)

# Start the watcher thread
threading.Thread(target=watch_folder, args=(os.path.join(os.getcwd(), 'input'),), daemon=True).start()

# Start the app
eel.start('index.html')
