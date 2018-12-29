import client

class responce:
    status_code = None
    def __init__(self,code):
        self.status_code = code

def test_check_responce():
    try:
        res = responce(400)
        client.Client._check_response(res)
    except client.BadRequest:
        pass
        #that is the error we are expecting in this case
