import utils
from aggregation.AggregationStrategy import AggregationStrategy
from collections import defaultdict
from datetime import datetime


class DetailAggregation(AggregationStrategy):
    def aggregate(self, data):
        results = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float)))))
        for file_name, date_data in data.items():
            for date, categories in date_data.items():
                for category, tasks in categories.items():
                    for task, task_data in tasks.items():
                        for key, val in task_data.items():
                            try:
                                results[file_name]["file_total"][key] = (
                                    results[file_name].get("file_total", {}).get(key, 0) + val
                                )
                                results[file_name][date]["day_total"][key] = (
                                    results[file_name][date].get("day_total", {}).get(key, 0) + val
                                )
                                results[file_name][date][category]["category_total"][key] = (
                                    results[file_name][date][category].get("category_total", {}).get(key, 0) + val
                                )
                                results[file_name][date][category][task][key] = (
                                    results[file_name][date][category].get(key, 0) + val
                                )
                            except TypeError:
                                print(
                                    f"Error with file_name={file_name}, date={date}, category={category}, task={task}, key={key}, val={val}"
                                )
                                raise
        return results

    def to_html(self, data, depth=0):
        if isinstance(data, dict):
            if "plan" in data.keys() or "done" in data.keys():
                html = "<table><tbody><tr>"
                for key in ["plan", "done"]:
                    html += f'<th class="level{depth + 2}">{key}</th>'
                html += "</tr><tr>"
                for key in ["plan", "done"]:
                    html += f"<td>{data.get(key, 0)}</td>"  # Use get method to avoid KeyError
                html += "</tr></tbody></table>"
            else:
                html = "<table><tbody>"
                date_keys = [key for key in data.keys() if utils.is_date(key)]
                non_date_keys = [key for key in data.keys() if not utils.is_date(key)]

                if date_keys:
                    date_keys = sorted(
                        date_keys,
                        key=lambda x: datetime.strptime(x, "%Y/%m/%d"),
                        reverse=True,
                    )
                keys = non_date_keys + date_keys

                for key in keys:
                    val = data[key]
                    tr_class = '<tr class="total">' if "_total" in key else "<tr>"
                    html += f'{tr_class}<th class="level{depth + 1}">{key}</th>'
                    html += f"<td>{self.to_html(val, depth + 1)}</td></tr>"

                html += "</tbody></table>"
            return html
        else:
            return str(data)
