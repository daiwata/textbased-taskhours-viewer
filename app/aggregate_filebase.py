from collections import defaultdict
from collections import OrderedDict

def aggregate_filebase(data):
    results = defaultdict(lambda: defaultdict(lambda: defaultdict(OrderedDict)))
    for file_name, date_data in data.items():
        for date, categories in date_data.items():
            for category, tasks in categories.items():
                for task, task_data in tasks.items():
                    for key, val in task_data.items():
                        try:
                            results[file_name]['file_total'][key] = results[file_name].get('file_total', {}).get(key, 0) + val
                            results[file_name][category]['category_total'][key] = results[file_name][category].get('category_total', {}).get(key, 0) + val
                            results[file_name][category][task][key] = results[file_name][category][task].get(key, 0) + val
                        except TypeError:
                            print(f"Error with file_name={file_name}, category={category}, task={task}, key={key}, val={val}")
                            raise
    return results