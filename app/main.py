import eel
import os
import threading
import time
import json
import sys
import aggr
import conv_detail
import conv_filebase
import conv_monthly
import aggregate_detail
import aggregate_filebase
import aggregate_monthly

DATA_CONFS = json.load(open('settings.json', 'r', encoding='utf-8'))
OUTJSON_PATH = "output/out.json"
current_html = {
    "detail_aggregated": "",
    "filebase_aggregated": "",
    "monthly_aggregated": ""
}

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
    
@eel.expose
def get_current_html():
    return current_html

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
        
        detail_aggregated_data = aggregate_detail.aggregate_detail(outJson)
        writeFile("output/detail.json", detail_aggregated_data)
        detail_aggregated_html = conv_detail.detail_json_to_html(detail_aggregated_data)
        writeFile("output/detail.html", detail_aggregated_html)
        current_html["detail_aggregated"] = detail_aggregated_html
        eel.detail_aggregated(detail_aggregated_html)

        # Generate the filebase aggregated HTML
        filebase_aggregated_data = aggregate_filebase.aggregate_filebase(outJson)
        writeFile("output/filebase_aggregated.json", filebase_aggregated_data)
        filebase_aggregated_html = conv_filebase.json_to_html_filebased_aggregated(filebase_aggregated_data)
        writeFile("output/filebase_aggregated.html", filebase_aggregated_html)
        current_html["filebase_aggregated"] = filebase_aggregated_html
        eel.filebase_aggregated(filebase_aggregated_html)

        # Generate the monthly aggregated HTML
        monthly_aggregated_data = aggregate_monthly.aggregate_monthly(outJson)
        writeFile("output/monthly_aggregated.json", monthly_aggregated_data)
        monthly_aggregated_html = conv_monthly.json_to_html_monthly_aggregated(monthly_aggregated_data)
        writeFile("output/monthly_aggregated.html", monthly_aggregated_html)
        current_html["monthly_aggregated"] = monthly_aggregated_html
        eel.monthly_aggregated(monthly_aggregated_html)

        time.sleep(1)

if os.path.exists(OUTJSON_PATH): os.remove(OUTJSON_PATH)

# Start the watcher thread
threading.Thread(target=watch_folder, args=(os.path.join(os.getcwd(), 'input'),), daemon=True).start()

# Start the app
eel.start('index.html')
