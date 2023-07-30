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
                                    results[year_month].get("month_total", {}).get(key, 0) + val
                                )
                                results[year_month][category]["category_total"][key] = (
                                    results[year_month][category].get("category_total", {}).get(key, 0) + val
                                )
                                results[year_month][category][task][key] = (
                                    results[year_month][category][task].get(key, 0) + val
                                )
                            except TypeError:
                                print(
                                    f"Error with year_month={year_month}, category={category}, task={task}, key={key}, val={val}"
                                )
                                raise

        results = OrderedDict(sorted(results.items(), reverse=True))

        return results

    def to_html(self, data):
        if isinstance(data, dict):
            if "plan" in data.keys() or "done" in data.keys():
                html = "<table class='plandone'><tbody><tr>"
                for key in ["plan", "done"]:
                    html += f'<th class="plandone">{key}</th>'
                html += "</tr><tr>"
                for key in ["plan", "done"]:
                    html += f"<td>{data.get(key, 0)}</td>"
                html += "</tr></tbody></table>"
            else:
                html = "<table><tbody>"
                for key, val in data.items():
                    html += f'<tr class="{"total" if "_total" in key else ""}">'
                    html += f'<th class="{key if "_total" in key else ""}">{key}</th>'
                    html += f'<td class="{"total" if "_total" in key else ""}">{self.to_html(val)}</td></tr>'
                html += "</tbody></table>"
            return html
        else:
            return str(data)
