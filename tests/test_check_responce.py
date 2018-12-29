from arcus import Client, exc


class responce:
    status_code = None

    def __init__(self, code):
        self.status_code = code

    # arbitrary data for UnprocessableEntity Exception
    def json(self):
        data = {
            "code": 5,
            "message": "this is message",
            "id": 8
        }
        return data


errors = {
    "400": exc.BadRequest,
    "401": exc.InvalidAuth,
    "403": exc.Forbidden,
    "404": exc.NotFound,
    "429": exc.TooManyRequests,
    "500": exc.InternalServerError,
    "503": exc.ServiceUnavailable
}


def test_check_responce():
    for code, err in errors.items():
        try:
            res = responce(int(code))
            Client._check_response(res)
        except err:
            pass

    try:
        res = responce(422)
        Client._check_response(res)
    except exc.UnprocessableEntity:
        pass
