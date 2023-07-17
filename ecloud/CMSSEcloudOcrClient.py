import base64
import requests
import json
from .Signature import sign
from requests.packages import urllib3


urlset1 = {"/api/ocr/v1/webimage", "/api/ocr/v1/idcard","/api/ocr/v1/businesslicense","/api/ocr/v1/enterpriselicense","/api/ocr/v1/generic",\
    "/api/ocr/v1/trainticket","/api/ocr/v1/invoice","/api/ocr/v1/licenseplate","/api/ocr/v1/ammeter","/api/ocr/v1/seal"}

urlset2 = {"/api/ocr/v1/general","/api/ocr/v1/handwriting","/api/ocr/v1/bankcard","/api/ocr/v1/businesscard","/api/ocr/v1/form",\
    "/api/ocr/v1/taxiinvoice","/api/ocr/v1/fixedinvoice","/api/ocr/v1/flights","/api/ocr/v1/toll","/api/ocr/v1/mixedbills","/api/ocr/v1/sealrecognition",\
        "/api/ocr/v1/driving","/api/ocr/v1/drive","/api/ocr/v1/vincode","/api/ocr/v1/formula", "/api/ocr/v1/smartstructure"}
urlset3 = {"/api/ocr/v1/selfdefinition"}

class CMSSEcloudOcrClient(object):

    def __init__(self, ak, sk, url):
        self.accesskey = ak
        self.secretkey = sk
        self.httpmethod = 'POST'
        self.hostname = url

    def request_ocr_service_file(self, requestpath, imagepath, options = None):
        urllib3.disable_warnings()
        querystring = sign('POST',self.accesskey, self.secretkey, requestpath)
        params = ''
        for(k,v) in querystring.items():
            params += str(k) + '=' + str(v) + '&'
        params = params[:-1]

        body = {}
        with open(imagepath, 'rb') as f:
            img = f.read()
        img_base64 = base64.b64encode(img).decode('utf-8')
        if requestpath in urlset1:
            body['imageFile'] = img_base64
        elif requestpath in urlset2:
            body['image'] = img_base64
        elif requestpath in urlset3:
            body['Image'] = img_base64
            templateid = options['TemplateId']
            body['TempalteId'] = templateid
        if options:
            body.update(options)
        url = self.hostname + requestpath + '?' + params
        s = requests.session()
        s.keep_alive = False
        response = requests.post(url, data = json.dumps(body), headers = {"Content-Type":"application/json"}, timeout = (5, 60),verify = False)
        return response

    def request_ocr_service_base64(self, requestpath, base64, options = None):
        urllib3.disable_warnings()
        querystring = sign('POST',self.accesskey, self.secretkey, requestpath)
        params = ''
        for(k,v) in querystring.items():
            params += str(k) + '=' + str(v) + '&'
        params = params[:-1]

        body = {}
        if requestpath in urlset1:
            body['imageFile'] = base64
        elif requestpath in urlset2:
            body['image'] = base64
        elif requestpath in urlset3:
            body['Image'] = base64
            templateid = options['TemplateId']
            body['TemplateId'] = templateid
        if options:
            body.update(options)
        url = self.hostname + requestpath + '?' + params
        s = requests.session()
        s.keep_alive = False
        response = requests.post(url, data = json.dumps(body), headers = {"Content-Type":"application/json"}, timeout = (5, 60), verify = False)
        return response


    def request_ocr_service_url(self, requestpath, imageurl, options = None):
        urllib3.disable_warnings()
        querystring = sign('POST',self.accesskey, self.secretkey, requestpath)
        params = ''
        for(k,v) in querystring.items():
            params += str(k) + '=' + str(v) + '&'
        params = params[:-1]

        body = {}
        if requestpath in urlset1:
            body['url'] = imageurl
        elif requestpath in urlset2:
            body['url'] = imageurl
        elif requestpath in urlset3:
            body['Url'] = imageurl
            templateid = options['TemplateId']
            body['TemplateId'] = templateid
        if options:
            body.update(options)
        url = self.hostname + requestpath + '?' + params
        s = requests.session()
        s.keep_alive = False
        response = requests.post(url, data = json.dumps(body), headers = {"Content-Type":"application/json"}, timeout = (5, 60),verify = False)
        return response