def toInt(string):
    if not string:
        return None
    try:
        return int(string)
    except ValueError:
        pass

    return None
