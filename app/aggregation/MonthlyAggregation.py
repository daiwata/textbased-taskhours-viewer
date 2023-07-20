from aggregation.AggregationStrategy import AggregationStrategy
from collections import defaultdict
from collections import OrderedDict
from datetime import datetime


class MonthlyAggregation(AggregationStrategy):
    def aggregate(self, data):
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
                                    results[year_month]
                                    .get("month_total", {})
                                    .get(key, 0)
                                    + val
                                )
                                results[year_month][category]["category_total"][key] = (
                                    results[year_month][category]
                                    .get("category_total", {})
                                    .get(key, 0)
                                    + val
                                )
                                results[year_month][category][task][key] = (
                                    results[year_month][category][task].get(key, 0)
                                    + val
                                )
                            except TypeError:
                                print(
                                    f"Error with year_month={year_month}, category={category}, task={task}, key={key}, val={val}"
                                )
                                raise

        # Sort the monthly aggregated data in reverse order by the year and month
        results = OrderedDict(sorted(results.items(), reverse=True))

        return results

    def to_html(self, data, depth=0):
        # conv_monthly.py の内容
        """
        Generate HTML from the monthly aggregated data dictionary.
        """
        if isinstance(data, dict):
            if "plan" in data.keys() or "done" in data.keys():
                # If 'plan' and 'done' are keys, transpose the row
                html = "<table><tbody><tr>"
                for key in ["plan", "done"]:
                    html += '<th class="level' + str(depth + 2) + '">' + key + "</th>"
                html += "</tr><tr>"
                for key in ["plan", "done"]:
                    html += (
                        "<td>" + str(data.get(key, 0)) + "</td>"
                    )  # Use get method to avoid KeyError
                html += "</tr></tbody></table>"
            else:
                html = "<table><tbody>"
                for key, val in data.items():
                    html += '<tr class="total">' if "_total" in key else "<tr>"
                    html += (
                        '<th class="level'
                        + str(depth + 1)
                        + '">'
                        + str(key)
                        + "</th><td>"
                        + self.to_html(val, depth + 1)
                        + "</td></tr>"
                    )
                html += "</tbody></table>"
            return html
        else:
            return str(data)
