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
                            monthly_aggregated_data[year_month]['month_total'][key] = monthly_aggregated_data[year_month].get('month_total', {}).get(key, 0) + val
                            monthly_aggregated_data[year_month][category]['category_total'][key] = monthly_aggregated_data[year_month][category].get('category_total', {}).get(key, 0) + val
                            monthly_aggregated_data[year_month][category][task][key] = monthly_aggregated_data[year_month][category][task].get(key, 0) + val
                        except TypeError:
                            print(f"Error with year_month={year_month}, category={category}, task={task}, key={key}, val={val}")
                            raise

    # Sort the monthly aggregated data in reverse order by the year and month
    monthly_aggregated_data = OrderedDict(sorted(monthly_aggregated_data.items(), reverse=True))

    return monthly_aggregated_data
