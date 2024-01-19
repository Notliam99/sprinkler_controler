from piApi import Api


api = Api()


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
    doc = f'''
        <center>
            <h1>Hello World<h1>
            <hr>
            <p>{request}</p>
        </center>
    '''
    return doc, 200


def Main():
    api.run(80)


if __name__ == '__main__':
    Main()
