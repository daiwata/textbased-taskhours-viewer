from collections import defaultdict
from collections import OrderedDict
from datetime import datetime 

def monthly_aggregate_data(data):
    monthly_aggregated_data = defaultdict(lambda: defaultdict(lambda: defaultdict(OrderedDict)))
    for file_name, date_data in data.items():
        for date_str, categories in date_data.items():
            date = datetime.strptime(date_str, "%Y/%m/%d")
            year_month = date.strftime("%Y/%m")
            for category, tasks in categories.items():
                for task, task_data in tasks.items():
                    for key, val in task_data.items():
                        try:
                            monthly_aggregated_data[year_month][category][task][key] = monthly_aggregated_data[year_month][category][task].get(key, 0) + val
                        except TypeError:
                            print(f"Error with year_month={year_month}, category={category}, task={task}, key={key}, val={val}")
                            raise

    # Sort the monthly aggregated data in reverse order by the year and month
    monthly_aggregated_data = OrderedDict(sorted(monthly_aggregated_data.items(), reverse=True))

    return monthly_aggregated_data


def json_to_html_monthly_aggregated(data, depth=0):
    """
    Generate HTML from the monthly aggregated data dictionary.
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
                html += '<tr><th class="level' + str(depth+1) + '">' + str(key) + '</th><td>' + json_to_html_monthly_aggregated(val, depth+1) + '</td></tr>'
            html += '</tbody></table>'
        return html
    else:
        return str(data)
