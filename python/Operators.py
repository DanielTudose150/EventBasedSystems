def number_allowed_operators():
    return ['<', '>', '<=', '>=', '=', '!=']


def string_allowed_operators():
    return ['=', '!=']


AllowedOperators = {
    'stationid': number_allowed_operators,
    'city': string_allowed_operators,
    'temperature': number_allowed_operators,
    'rain': number_allowed_operators,
    'wind': number_allowed_operators,
    'direction': string_allowed_operators,
    'date': string_allowed_operators,
}
