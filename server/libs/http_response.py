
def response(data, code=200):
    if code is None:
        code = 200
    res = {
        'code': code,
        'data': data,
    }
    return res
