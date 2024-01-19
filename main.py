from piApi import Api
import ujson


api = Api()


sprincklers = {
    "0": {
        "status": False
    },
    "1": {
        "status": False
    },
    "2": {
        "status": False
    },
    "3": {
        "status": False
    }
}


def parse_url_prams(raw_path: str) -> dict:
    if len(raw_path.split('?')) < 2:
        return {}
    url_params = raw_path.split("?")[1].split('&')
    prams = dict()
    for i in url_params:
        pram = i.split('=')
        prams[f"{pram[0]}"] = f"{pram[1]}"
    return prams


@api.get('/')
def hello_world(request):
    """
        Index route decorated by @api.get()
        ARGS:
            request: dict # contains the parsed request
        RETURNS:
            document: str
            responce_code: int # optional
            custom_headers: dict # optional Requries( responce_code )
    """
    try:
        with open("./spricklerUI/index.html") as file:
            html = file.read()
            file.close()
            return html, 200
    except Exception as error:
        print(f"ERROR: {error}")
        return error, 501


@api.get('/sprinckler/status')
def sprickler_status(request):
    prams = parse_url_prams(request['raw_path'])
    print(prams)
    try:
        specifed_data = sprincklers[prams['id']]
    except Exception as e:
        print(e)
        specifed_data = sprincklers
    json_data = ujson.dumps(specifed_data)
    return json_data, 200, {'Content-Type': 'application/json'}


def Main():
    api.run(80)


if __name__ == '__main__':
    Main()
