from piApi import Api
from machine import Pin
import ujson


led = Pin("LED", Pin.OUT)
api = Api()


sprincklers = {
    "0": {
        "status": False,
        "gpio": 13
    },
    "1": {
        "status": False,
        "gpio": 14
    },
    "2": {
        "status": False,
        "gpio": 15
    },
    "3": {
        "status": False,
        "gpio": 16
    }
}


def sprinckler_switch(status):
    for key in status.keys():
        data = status[key]
        pin = Pin(data["gpio"], Pin.OUT)
        pin.value(data["status"])


def led_indicator(func):
    def wrapper(*args, **kwagrs):
        led.off()
        value = func()
        led.on()
        return value
    return wrapper


def parse_url_prams(raw_path: str) -> dict:
    if len(raw_path.split('?')) < 2:
        return {}
    url_params = raw_path.split("?")[1].split('&')
    prams = dict()
    for i in url_params:
        pram = i.split('=')
        prams[f"{pram[0]}"] = f"{pram[1]}"
    return prams


@led_indicator
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


@led_indicator
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


@led_indicator
@api.post('/sprinckler/toggle')
def sprickler_toggle(request):
    prams = parse_url_prams(request['raw_path'])
    print(prams)
    try:
        if prams['id'] == 'all':
            for i in sprincklers.keys():
                sprincklers[i]['status'] = (not sprincklers[i]['status'])

        sprincklers[prams['id']]['status'] = (
            not sprincklers[prams['id']]['status'])
    except Exception as e:
        print(e)
    sprinckler_switch(sprincklers)
    return '{"woow": "w00w"}', 200


def Main():
    led.on()
    api.run(80)


if __name__ == '__main__':
    Main()
