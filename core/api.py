


def f_request(inter, line, args, **kwargs):
    import requests

    # get URL to request from
    url = inter.parse(0, line, args)[2]
    # url must be str
    inter.type_err([(url, (str,))], line, kwargs["lines_ran"])
    try:
        # get parameters
        params = inter.parse(1, line, args)[2]
    except:
        params = None
    r = requests.get(url=url, params=params)
    # return response
    try:
        return r.json()
    except:
        return r

def f_pubip(inter, line, args, **kwargs):
    import requests
    
    # asks an api server for this address
    return requests.get("https://api.ipify.org").text
def f_privip(inter, line, args, **kwargs):
    import socket
    
    # gets the private ips of this machine
    return socket.gethostbyname_ex(socket.gethostname())[2]
def f_endpoint(inter, line, args, **kwargs):
    # imports
    from flask import Flask
    from flask_restful import Api, Resource
    import logging
    
    # initial API endpoint data
    path = None
    init_data = {}
    port = 5000
    host = "127.0.0.1"
    last_arg = None
    # 1 argument, defaults to 127.0.0.1:5000/path = {}
    if len(args) == 1:
        # path to endpoint
        path = inter.parse(0, line, args)[2]
        # path should be str
        inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
        last_arg = path
    # 2 arguments, defaults to 127.0.0.1:5000/path = init_data
    if len(args) == 2:
        # path to endpoint
        path = inter.parse(0, line, args)[2]
        # path should be str
        inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
        # json to initialize at the endpoint
        init_data = inter.parse(1, line, args)[2]
        # init_data should be dict
        inter.type_err([(init_data, (dict,))], line, kwargs["lines_ran"])
        last_arg = init_data
    # 3 arguments, defaults to host:port/path = init_data
    else:
        # host to endpoint as first argument
        host = inter.parse(0, line, args)[2]
        # host should be str
        inter.type_err([(host, (str,))], line, kwargs["lines_ran"])
        # port to endpoint as second argument
        port = inter.parse(1, line, args)[2]
        # port should be int
        inter.type_err([(port, (int,))], line, kwargs["lines_ran"])
        # path to endpoint
        path = inter.parse(2, line, args)[2]
        # path should be str
        inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
        # json to initialize at the endpoint
        init_data = inter.parse(3, line, args)[2]
        # init_data should be dict
        inter.type_err([(init_data, (dict,))], line, kwargs["lines_ran"])
        last_arg = init_data
        if len(args) == 5:
            last_arg = inter.parse(4, line, args)[2]
    # prepare endpoint
    print("serving on http://" + host + ":" + str(port) + path)
    app = Flask(__name__)
    cors = False
    # if the last argument is a string with 'CORS' in it
    # then enable CORS
    if isinstance(last_arg, str) and "CORS" in last_arg:
        from flask_cors import CORS

        # enable CORS
        print("starting with cors")
        cors = True
        CORS(app)
    # disable flask messages that aren't error-related
    log = logging.getLogger("werkzeug")
    log.disabled = True
    app.logger.disabled = True
    # gets Flask Api
    api = Api(app)
    # api endpoint class
    
    class EndPoint(Resource):
        @classmethod
        def make_api(cls, response):
            cls.response = response
            return cls
        
        # GET
        def get(self):
            return self.response
        
        # POST
        def post(self):
            from flask import request
            
            # obtains current endpoint data
            current_data = self.response
            # updates current data with data to post
            current_data.update(request.get_json())
            # updates next response
            self.make_api(current_data)
            return current_data
        
        # DELETE
        def delete(self):
            self.make_api({})
            return self.response
        
    curr_endpoint = EndPoint.make_api(init_data)
    # logs newly created endpoint
    inter.endpoints[path] = api
    # adds class EndPoint as a Resource to the Api with the specific path
    # passes arg2 alongside
    api.add_resource(curr_endpoint, path)
    
    # starting flask server
    try:
        # if internal
        app.run(host=host, port=port, debug=False)
    except:
        # if external
        try:
            app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
        except:
            None
    return api
def f_post(inter, line, args, **kwargs):
    import requests
    
    # url to post to, defaults to localhost
    host = inter.parse(0, line, args)[2]
    # host must be str
    inter.type_err([(host, (str,))], line, kwargs["lines_ran"])
    # port to post to
    port = inter.parse(1, line, args)[2]
    # port must be int
    inter.type_err([(port, (int,))], line, kwargs["lines_ran"])
    # path after url
    path = inter.parse(2, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    # data to post
    data = inter.parse(3, line, args)[2]
    # data must be dict
    inter.type_err([(data, (dict,))], line, kwargs["lines_ran"])
    # if local network
    if host == "0.0.0.0":
        response = requests.post(
            url=("http://127.0.0.1:" + str(port) + path), json=data
        )
    # if localhost
    else:
        # post to endpoint
        response = requests.post(
            url=("http://" + host + ":" + str(port) + path), json=data
        )
    # get response
    return response.json()
def f_get_api(inter, line, args, **kwargs):
    import requests
    
    # url to get from, defaults to localhost
    host = inter.parse(0, line, args)[2]
    # host must be str
    inter.type_err([(host, (str,))], line, kwargs["lines_ran"])
    # port to get from
    port = inter.parse(1, line, args)[2]
    # port must be int
    inter.type_err([(port, (int,))], line, kwargs["lines_ran"])
    # path after url
    path = inter.parse(2, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    # if local network
    if host == "0.0.0.0":
        return requests.get(
            url=("http://127.0.0.1:" + str(port) + path)
        ).json()
    # if localhost
    else:
        return requests.get(
            url=("http://" + host + ":" + str(port) + path)
        ).json()
def f_delete(inter, line, args, **kwargs):
    import requests
    
    # url to delete from, defaults to localhost
    host = inter.parse(0, line, args)[2]
    # host must be str
    inter.type_err([(host, (str,))], line, kwargs["lines_ran"])
    # port to delete from
    port = inter.parse(1, line, args)[2]
    # port must be int
    inter.type_err([(port, (int,))], line, kwargs["lines_ran"])
    # path after url
    path = inter.parse(2, line, args)[2]
    # path must be str
    inter.type_err([(path, (str,))], line, kwargs["lines_ran"])
    if host == "0.0.0.0":
        response = requests.delete(
            url=("http://127.0.0.1:" + str(port) + path)
        )
    else:
        # delete from endpoint
        response = requests.delete(
            url=("http://" + host + ":" + str(port) + path)
        )
    return response.json()


API_DISPATCH = {
    "request": f_request,
    "pubip": f_pubip,
    "privip": f_privip,
    "ENDPOINT": f_endpoint,
    "POST": f_post,
    "DELETE": f_delete,
    "GET": f_get_api,
}