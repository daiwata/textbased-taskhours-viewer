import os
import json
import re
import glob
from operator import itemgetter

DATA_CONFS = json.load(open('settings.json', 'r', encoding='utf-8'))

def addActualHours(data, fName, dateStr, type, taskName, kind, hours):
    savedDates = data.get(fName, {})
    savedTypes = savedDates.get(dateStr, {})
    savedTasks = savedTypes.get(type, {})
    savedLines = savedTasks.get(taskName, {})
    data = { 
        **data, 
        fName: {
            **savedDates,
            dateStr: { 
                **savedTypes,
                type: {
                **savedTasks, 
                    taskName: {
                        **savedLines, 
                        kind: savedLines.get(kind, 0) + hours
                    }
                }
            }
        }
    }
    return data

def addLineResult(data, fName, dateStr, lineStr):
    for conf in DATA_CONFS:
        type, sepPlan, sepDone = itemgetter('type', 'sepPlan', 'sepDone')(conf)
        taskName = ""
        if lineStr.startswith(sepPlan):
            regexPlan = r"^[" + re.escape(sepPlan) + r"\s]+"
            taskName = re.sub(regexPlan, '', lineStr)
            hours = len(lineStr.replace(taskName, "").replace(" ", "")) / 4
            data = addActualHours(data, fName, dateStr, type, taskName, "plan", hours)
            data["savedTaskName"] = taskName
        elif lineStr.startswith(sepDone):
            regexDone = r"^[" + re.escape(sepDone) + r"\s]+"
            taskNameTmp = re.sub(regexDone, '', lineStr).strip()
            taskName = taskNameTmp if taskNameTmp != "" else data.get("savedTaskName")
            hours = len(lineStr.replace(taskName, "").replace(" ", "")) / 4
            data = addActualHours(data, fName, dateStr, type, taskName, "done", hours)
    return data

def calcDateStr(lineStr, dateStr):
    if lineStr.startswith("2023"):
        dateStr = lineStr
    return dateStr

def analyzeTxt():
    data = {}
    dateStr = ""
    pathList = glob.glob("input/*.txt")
    for fPath in pathList:
        with open(fPath, 'r', encoding='utf-8') as f:
            for lineRaw in f:
                fName = os.path.basename(fPath) 
                lineStr = lineRaw.strip()
                dateStr = calcDateStr(lineStr, dateStr);
                data = addLineResult(data, fName, dateStr, lineStr)
    data.pop("savedTaskName")
    return data
