########### Python 2.7 #############
import httplib
import urllib
import base64
import urlparse
import json

def parseresult(results = []):
    stringBuilder = "Text: "
    if (results != [] and len(results["regions"]) > 0):
        stringBuilder += "\n"
        for item in results["regions"]:
            for line in item["lines"]:
                for word in line["words"]:
                    stringBuilder += word["text"]
                    stringBuilder += " "
                stringBuilder += "\n"
            stringBuilder += "\n"
    return stringBuilder


fpath = "c:\\tests\\mytest.png"

headers = {
   'Content-type': 'application/octet-stream',
}

params = urllib.urlencode({
   # Specify your subscription key
   'subscription-key': 'xxxxxxxx',
   # Specify values for optional parameters, as needed
   'language': 'en',
   #'detectOrientation ': 'true',
})

try:
   conn = httplib.HTTPSConnection('api.projectoxford.ai')
   conn.request("POST", "/vision/v1/ocr?%s" % params, open(fpath, "rb"), headers)
   response = conn.getresponse()
   data = response.read()
   print(data)
   conn.close()
except Exception as e:
   print("[Errno {0}] {1}".format(e.errno, e.strerror))

result = parseresult(json.loads(data))
print(result)
print("done!")