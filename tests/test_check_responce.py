from arcus import Client, exc


class responce:
    status_code = None

    def __init__(self, code):
        self.status_code = code


def test_check_responce():
    try:
        res = responce(400)
        Client._check_response(res)
    except exc.BadRequest:
        pass
