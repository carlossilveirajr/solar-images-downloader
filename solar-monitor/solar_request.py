import json
from datetime import date

import requests

import request_parser
from utils.data_utils import date_range


def create_request(request_date):
    return "https://www.solarmonitor.org/?date=" + request_date.strftime("%Y%m%d")


def get_sunspots_for(day):
    url = create_request(day)
    request = requests.get(url)
    return request_parser.extract_sunspot_per_day(day, request.content)


def daily_sunspots_to_individual_sunspot(spots_per_day):
    positions = spots_per_day['positions']
    number_of_spots = len(positions)

    parsed_date = spots_per_day['date'].strftime("%Y%m%d")

    for i in range(number_of_spots):
        yield {
            'date': parsed_date,
            'id': spots_per_day['ids'][i],
            'position': positions[i],
            'mcintosh': spots_per_day['mcintoshs'][i],
            'hale': spots_per_day['hales'][i],
            'area': spots_per_day['areas'][i],
            'nspots': spots_per_day['nspots'][i]
        }


def write_to_json(spots, file_name):
    with open(file_name, "a", encoding='utf-8') as f:
        for s in spots:
            json.dump(s, f)
            f.write("\n")


def progress(count, total):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    print('\r[%s] %s%s ...%s / %s ' % (bar, percents, '%', count, total), end="")


def main(first_date, last_date, file_name):
    total = (last_date - first_date).days
    count = 0

    for d in date_range(first_date, last_date):
        spots_per_day = get_sunspots_for(d)
        spots = daily_sunspots_to_individual_sunspot(spots_per_day)

        write_to_json(spots, file_name)

        count += 1
        progress(count, total)


if __name__ == '__main__':
    end_date = date(2022, 6, 1)
    start_date = date(2010, 7, 1)
    main(start_date, end_date, "target/sunspots.json")
