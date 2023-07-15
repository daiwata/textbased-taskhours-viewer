from collections import defaultdict
from collections import OrderedDict

from collections import defaultdict

def detail_aggregate_data(data):
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


def detail_json_to_html(data, depth=0):
    """
    Generate HTML from the detailed aggregated data dictionary.
    """
    if isinstance(data, dict):
        if 'plan' in data.keys() or 'done' in data.keys():
            html = '<table><tbody><tr>'
            for key in ['plan', 'done']:
                html += '<th class="level' + str(depth+2) + '">' + key + '</th>'
            html += '</tr><tr>'
            for key in ['plan', 'done']:
                html += '<td>' + str(data.get(key, 0)) + '</td>'  # Use get method to avoid KeyError
            html += '</tr></tbody></table>'
        else:
            html = '<table><tbody>'
            for key, val in data.items():
                html += '<tr class="total">' if "_total" in key else '<tr>'
                html += '<th class="level' + str(depth+1) + '">' + str(key) + '</th><td>' + detail_json_to_html(val, depth+1) + '</td></tr>'
            html += '</tbody></table>'
        return html
    else:
        return str(data)
