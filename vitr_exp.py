import requests
import json

api_key = ''
url_all = 'http://json.lavitrine.com/lavitrinejsonapi?key=%s&command=get_activities&maxcount=500000' % api_key
url = 'http://json.lavitrine.com/lavitrinejsonapi?key=%s&command=get_activity&maxcount=500000&id=%s'

all_ids = requests.get(url_all)

w_ids = []

with open('event_ids.json', 'w') as w_file:
    for row in all_ids.json():
        evid = row.get('id')
        w_ids.append(evid)
        print('Got id %s' % evid)

    json.dump(w_ids, w_file)

ev_locs = []

for wid in w_ids:
    r = requests.get(url % (api_key, wid))
    dat = r.json()

    try:
        new_row = {
            'title': dat.get('title'),    
            'latitude': dat.get('showings')[0].get('location').get('latitude'),
            'longitude': dat.get('showings')[0].get('location').get('longitude'),
            'start': dat.get('showings')[0].get('start_date'),
            'end': dat.get('showings')[0].get('end_date'),
        }
        print(new_row)
        ev_locs.append(new_row)

    except Exception as ex:
        print(ex)


with open('ev_locs.csv', 'w') as w_csv:
    title_str = ""
    val_rows = []
    for item in ev_locs:
        val_str = ""
        for key, value in item.items():
            # Set the title
            val_str += value

            if value != list(item.values())[-1]:
                val_str += ","

        val_rows.append(val_str)

    for key in list(ev_locs[0].keys()):
        title_str += key

        if key != list(ev_locs[0].keys())[-1]:
                title_str += ","




    title_str += "\n"
    w_csv.write(title_str)

    for row in val_rows:
        row += "\n"
        print("Wrote %s to file" % row)
        w_csv.write(row)



