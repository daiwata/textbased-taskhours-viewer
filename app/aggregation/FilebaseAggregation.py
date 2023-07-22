from aggregation.AggregationStrategy import AggregationStrategy
from collections import defaultdict
from collections import OrderedDict


class FilebaseAggregation(AggregationStrategy):
    def aggregate(self, data):
        results = defaultdict(lambda: defaultdict(lambda: defaultdict(OrderedDict)))
        for file_name, date_data in data.items():
            for date, categories in date_data.items():
                for category, tasks in categories.items():
                    for task, task_data in tasks.items():
                        for key, val in task_data.items():
                            try:
                                results[file_name]["file_total"][key] = (
                                    results[file_name].get("file_total", {}).get(key, 0) + val
                                )
                                results[file_name][category]["category_total"][key] = (
                                    results[file_name][category].get("category_total", {}).get(key, 0) + val
                                )
                                results[file_name][category][task][key] = (
                                    results[file_name][category][task].get(key, 0) + val
                                )
                            except TypeError:
                                print(
                                    f"Error with file_name={file_name}, category={category}, task={task}, key={key}, val={val}"
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
                    html += f"<td>{data.get(key, 0)}</td>"
                html += "</tr></tbody></table>"
            else:
                html = "<table><tbody>"
                for key, val in data.items():
                    tr_class = '<tr class="total">' if "_total" in key else "<tr>"
                    html += f'{tr_class}<th class="level{depth + 1}">{key}</th>'
                    html += f"<td>{self.to_html(val, depth + 1)}</td></tr>"
                html += "</tbody></table>"
            return html
        else:
            return str(data)
