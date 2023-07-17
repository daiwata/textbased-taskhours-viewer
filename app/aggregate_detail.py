from collections import defaultdict
from datetime import datetime

def aggregate_detail(data):
    detail_aggregated_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float)))))
    for file_name, date_data in data.items():
        for date, categories in date_data.items():
            for category, tasks in categories.items():
                for task, task_data in tasks.items():
                    for key, val in task_data.items():
                        try:
                            if 'file_total' not in detail_aggregated_data[file_name]:
                                detail_aggregated_data[file_name]['file_total'] = defaultdict(float)
                            detail_aggregated_data[file_name]['file_total'][key] += val
                            
                            if 'day_total' not in detail_aggregated_data[file_name][date]:
                                detail_aggregated_data[file_name][date]['day_total'] = defaultdict(float)
                            detail_aggregated_data[file_name][date]['day_total'][key] += val
                            
                            if 'category_total' not in detail_aggregated_data[file_name][date][category]:
                                detail_aggregated_data[file_name][date][category]['category_total'] = defaultdict(float)
                            detail_aggregated_data[file_name][date][category]['category_total'][key] += val
                            
                            if task not in detail_aggregated_data[file_name][date][category]:
                                detail_aggregated_data[file_name][date][category][task] = defaultdict(float)
                            detail_aggregated_data[file_name][date][category][task][key] += val
                        except TypeError:
                            print(f"Error with file_name={file_name}, date={date}, category={category}, task={task}, key={key}, val={val}")
                            raise
    return detail_aggregated_data
