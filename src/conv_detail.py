from collections import defaultdict
from collections import OrderedDict
from datetime import datetime 

def detail_aggregate_data(data):
    aggregated_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(OrderedDict))))
    for file_name, date_data in data.items():
        for date_str, categories in date_data.items():
            date = datetime.strptime(date_str, "%Y/%m/%d")
            year_month = date.strftime("%Y/%m")
            for category, tasks in categories.items():
                for task, task_data in tasks.items():
                    for key, val in task_data.items():
                        try:
                            aggregated_data[file_name]['file_total'][key] = aggregated_data[file_name].get('file_total', {}).get(key, 0) + val
                            aggregated_data[file_name][year_month]['month_total'][key] = aggregated_data[file_name][year_month].get('month_total', {}).get(key, 0) + val
                            aggregated_data[file_name][year_month][category]['category_total'][key] = aggregated_data[file_name][year_month][category].get('category_total', {}).get(key, 0) + val
                            aggregated_data[file_name][year_month][category][task][key] = aggregated_data[file_name][year_month][category][task].get(key, 0) + val
                        except TypeError:
                            print(f"Error with file_name={file_name}, year_month={year_month}, category={category}, task={task}, key={key}, val={val}")
                            raise
    return aggregated_data

def detail_json_to_html(data, depth=0):
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
