import utils
from aggregation.AggregationStrategy import AggregationStrategy
from collections import defaultdict
from datetime import datetime


class DetailAggregation(AggregationStrategy):
    def aggregate(self, data):
        # aggregate_detail.py の内容

        results = defaultdict(
            lambda: defaultdict(
                lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
            )
        )
        for file_name, date_data in data.items():
            for date, categories in date_data.items():
                for category, tasks in categories.items():
                    for task, task_data in tasks.items():
                        for key, val in task_data.items():
                            try:
                                results[file_name]["file_total"][key] = (
                                    results[file_name].get("file_total", {}).get(key, 0)
                                    + val
                                )
                                results[file_name][date]["day_total"][key] = (
                                    results[file_name][date]
                                    .get("day_total", {})
                                    .get(key, 0)
                                    + val
                                )
                                results[file_name][category]["category_total"][key] = (
                                    results[file_name][category]
                                    .get("category_total", {})
                                    .get(key, 0)
                                    + val
                                )
                                results[file_name][category][task][key] = (
                                    results[file_name][category][task].get(key, 0) + val
                                )
                            except TypeError:
                                print(
                                    f"Error with file_name={file_name}, date={date}, category={category}, task={task}, key={key}, val={val}"
                                )
                                raise
        return results

    def to_html(self, data, depth=0):
        # conv_detail.py の内容

        """
        Generate HTML from the detailed aggregated data dictionary.
        """
        if isinstance(data, dict):
            if "plan" in data.keys() or "done" in data.keys():
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
                # Separate date keys and other keys
                date_keys = [key for key in data.keys() if utils.is_date(key)]
                non_date_keys = [key for key in data.keys() if not utils.is_date(key)]
                # If there are any date keys, sort them
                if date_keys:
                    date_keys = sorted(
                        date_keys,
                        key=lambda x: datetime.strptime(x, "%Y/%m/%d"),
                        reverse=True,
                    )
                # Combine keys: non-date keys first, then sorted date keys
                keys = non_date_keys + date_keys
                for key in keys:
                    val = data[key]
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
