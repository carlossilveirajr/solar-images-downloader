
def __extract_pre_formatted_attribute(attribute_name, lines):
    return [line[45:]
            for line in lines
            if ("id=\"%s\"" % attribute_name) in line]


def extract_positions(lines):
    pre_formatted_attribute = __extract_pre_formatted_attribute("position", lines)
    return [p[:6] for p in pre_formatted_attribute]


def __extract_attribute_value(attribute_name, lines):
    pre_formatted_lines = __extract_pre_formatted_attribute(attribute_name, lines)
    return [p.split("/")[0] for p in pre_formatted_lines]


def extract_mcintosh(lines):
    return __extract_attribute_value("mcintosh", lines)


def extract_hale(lines):
    return __extract_attribute_value("hale", lines)


def extract_area(lines):
    return __extract_attribute_value("area", lines)


def extract_nspots(lines):
    return __extract_attribute_value("nspots", lines)


def extract_id(lines):
    result = list()
    for p in __extract_pre_formatted_attribute("noaa_number", lines):
        region = p.split("region=")[1]
        sunspot_id = region.split("\"")[0]
        result.append(sunspot_id)

    return result


def extract_sunspot_per_day(day, content):
    lines = str(content).split("\\n")
    return {
        "date": day,
        "positions": extract_positions(lines),
        "mcintoshs": extract_mcintosh(lines),
        "hales": extract_hale(lines),
        "areas": extract_area(lines),
        "nspots": extract_nspots(lines),
        "ids": extract_id(lines)
    }
