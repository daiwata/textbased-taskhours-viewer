from collections import defaultdict
from collections import OrderedDict

def filebase_aggregate_data(data):
    filebase_aggregated_data = defaultdict(lambda: defaultdict(lambda: defaultdict(OrderedDict)))
    for file_name, date_data in data.items():
        for date, categories in date_data.items():
            for category, tasks in categories.items():
                for task, task_data in tasks.items():
                    for key, val in task_data.items():
                        try:
                            filebase_aggregated_data[file_name]['file_total'][key] = filebase_aggregated_data[file_name].get('file_total', {}).get(key, 0) + val
                            filebase_aggregated_data[file_name][category]['category_total'][key] = filebase_aggregated_data[file_name][category].get('category_total', {}).get(key, 0) + val
                            filebase_aggregated_data[file_name][category][task][key] = filebase_aggregated_data[file_name][category][task].get(key, 0) + val
                        except TypeError:
                            print(f"Error with file_name={file_name}, category={category}, task={task}, key={key}, val={val}")
                            raise
    return filebase_aggregated_data

def json_to_html_filebased_aggregated(data, depth=0):
    """
    Generate HTML from the filebase aggregated data dictionary.
    """
    if isinstance(data, dict):
        if 'plan' in data.keys() or 'done' in data.keys():
            # If 'plan' and 'done' are keys, transpose the row
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
                html += '<th class="level' + str(depth+1) + '">' + str(key) + '</th><td>' + json_to_html_filebased_aggregated(val, depth+1) + '</td></tr>'
            html += '</tbody></table>'
        return html
    else:
        return str(data)
