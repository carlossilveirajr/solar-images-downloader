import psycopg2
import json

__create_table_if_does_exits = '''CREATE TABLE IF NOT EXISTS sunspot(
                                    sunspot_date CHAR(8)      NOT NULL,
                                    id           VARCHAR(10)  NOT NULL,
                                    position     VARCHAR(10),
                                    mcintosh     VARCHAR(5),
                                    hale         VARCHAR(100),
                                    area         VARCHAR(6),
                                    nspots       VARCHAR(6),
                                    
                                    PRIMARY KEY(sunspot_date, id)
                                );'''
__insert_sql = '''INSERT INTO sunspot(
                        sunspot_date,
                        id,
                        position,
                        mcintosh,
                        hale,
                        area,
                        nspots
                    ) VALUES (
                        %(date)s, 
                        %(id)s,
                        %(position)s,
                        %(mcintosh)s,
                        %(hale)s,
                        %(area)s,
                        %(nspots)s
                    )'''


def main(file_name):
    cursor = create_cursor()
    create_table_if_not_exists(cursor)
    for s in extract_sunspots_from(file_name):
        insert_json_to_postgres(s, cursor)


def extract_sunspots_from(file_name):
    lines = read_from_file(file_name)
    jsons = convert_to_json(lines)
    return remove_empty_sunspots(jsons)


def read_from_file(file_name):
    with open(file_name, "r", encoding='utf-8') as f:
        return f.readlines()


def convert_to_json(lines):
    return [json.loads(l) for l in lines]


def remove_empty_sunspots(sunspots):
    return [s for s in sunspots if s['mcintosh'] != '']


def create_cursor():
    conn = psycopg2.connect(
        database="postgres",
        user='postgres',
        password='password',
        host='localhost',
        port='5432'
    )
    conn.autocommit = True
    return conn.cursor()


def create_table_if_not_exists(cursor):
    cursor.execute(__create_table_if_does_exits)


def insert_json_to_postgres(data, cursor):
    cursor.execute(__insert_sql, data)


if __name__ == '__main__':
    main("target/sunspots.json")
