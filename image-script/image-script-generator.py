from datetime import date

from utils.data_utils import date_range

OUT_FILE_NAME = "../wgets.txt"
WGET_PREFIX = "wget -r --random-wait --accept-regex='[0-9_]_512_HMIB\.jpg' " \
                     "--no-parent https://sdo.gsfc.nasa.gov/assets/img/browse/"


def create_request(single_date):
    return WGET_PREFIX + single_date.strftime("%Y/%m/%d") + "\n"


def write_to_file(requests, file_name):
    with open(file_name, "w", encoding='utf-8') as f:
        f.writelines(requests)


def main(start_date, end_date):
    requests = [create_request(d) for d in date_range(start_date, end_date)]
    write_to_file(requests, OUT_FILE_NAME)


if __name__ == '__main__':
    main(date(2010, 7, 1), date(2022, 5, 31))
