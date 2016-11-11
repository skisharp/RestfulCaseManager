import requests


class RestRequest:
    def __init__(self, session):
        self.session = session

    def restGet(self, url):
        try:
            response = self.session.get(url)
            return response
        except requests.ConnectionError:
            print "Raise a ConnectionError!"
        except requests.HTTPError:
            print "Raise a HTTPError!"
        except requests.Timeout:
            print "Raise a Timeout Error!"
        except requests.TooManyRedirects:
            print "Raise a TooManyRedirects Error!"
        except:
            import traceback
            print(traceback.print_exc())

        return None

    def restPost(self, url, data, params=None):
        response = None
        try:
            # data type is unicode
            # data = data.encode('utf-8')
            # if data != "":
                # data = json.loads(data)
            # else:
                # data = {}
            # data type need dict
            # timeout
            # from requests import Request, Session
            # req = Request('POST', url, json=data)
            # prepped = self.session.prepare_request(req)

            # response = self.session.send(prepped, timeout=60)

            response = self.session.post(url, json=data, params=params)
        except requests.ConnectionError:
            print "Raise a ConnectionError!"
        except requests.HTTPError:
            print "Raise a HTTPError!"
        except requests.Timeout:
            print "Raise a Timeout Error!"
        except requests.TooManyRedirects:
            print "Raise a TooManyRedirects Error!"
        except:
            import traceback
            traceback.print_exc()
        return response

    def restPut(self, url, data, params=None):
        response = None
        try:
            response = self.session.put(url, json=data,params=params)
        except requests.ConnectionError:
            print "Raise a ConnectionError!"
        except requests.HTTPError:
            print "Raise a HTTPError!"
        except requests.Timeout:
            print "Raise a Timeout Error!"
        except requests.TooManyRedirects:
            print "Raise a TooManyRedirects Error!"
        return response
