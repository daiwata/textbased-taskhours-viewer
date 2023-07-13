import json

def json_to_html(data, depth=0):
    if isinstance(data, dict):
        if 'plan' in data.keys() or 'done' in data.keys():
            # If 'plan' and 'done' are keys, transpose the row
            html = '<table><tbody><tr>'
            for key in ['plan', 'done']:
                html += '<th class="level' + str(depth) + '">' + key + '</th>'
            html += '</tr><tr>'
            for key in ['plan', 'done']:
                if key in data:
                    html += '<td>' + str(data[key]) + '</td>'
                else:
                    # Display 0 if there is no data for 'plan' or 'done'
                    html += '<td>0</td>'
            html += '</tr></tbody></table>'
        else:
            html = '<table><tbody>'
            for key, val in data.items():
                html += '<tr><th class="level' + str(depth) + '">' + str(key) + '</th><td>' + json_to_html(val, depth+1) + '</td></tr>'
            html += '</tbody></table>'
        return html
    else:
        return str(data)