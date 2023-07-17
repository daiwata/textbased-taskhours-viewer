from collections import defaultdict
from collections import OrderedDict
from datetime import datetime


def aggregate_monthly(data):
    results = defaultdict(lambda: defaultdict(lambda: defaultdict(OrderedDict)))
    for file_name, date_data in data.items():
        for date_str, categories in date_data.items():
            date = datetime.strptime(date_str, "%Y/%m/%d")
            year_month = date.strftime("%Y/%m")
            for category, tasks in categories.items():
                for task, task_data in tasks.items():
                    for key, val in task_data.items():
                        try:
                            results[year_month]["month_total"][key] = (
                                results[year_month].get("month_total", {}).get(key, 0)
                                + val
                            )
                            results[year_month][category]["category_total"][key] = (
                                results[year_month][category]
                                .get("category_total", {})
                                .get(key, 0)
                                + val
                            )
                            results[year_month][category][task][key] = (
                                results[year_month][category][task].get(key, 0) + val
                            )
                        except TypeError:
                            print(
                                f"Error with year_month={year_month}, category={category}, task={task}, key={key}, val={val}"
                            )
                            raise

    # Sort the monthly aggregated data in reverse order by the year and month
    results = OrderedDict(sorted(results.items(), reverse=True))

    return results
