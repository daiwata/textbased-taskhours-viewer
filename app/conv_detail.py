from datetime import datetime
import utils


def detail_json_to_html(data, depth=0):
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
                    + detail_json_to_html(val, depth + 1)
                    + "</td></tr>"
                )
            html += "</tbody></table>"
        return html
    else:
        return str(data)
