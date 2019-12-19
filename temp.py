import http.client

conn = http.client.HTTPConnection("api,spotify,com")

headers = {
    'Authorization': "Bearer BQANgUUuqVNSmbTQHAjMAEczbY4nYDHggAjA9h_zh3drG2UCamKrywj85d2K9-SVAWC-MFJ3rTwtUnMeNDk-ZpAwssZkyPtdp5PWXs3v8NV-VA1gR5MVV7auEOuWjAXh3lHbccZZqW2g4GBi",
    'User-Agent': "PostmanRuntime/7.20.1",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "2ac98c4e-dd41-447a-8ddf-a0832b3bdb91,ccc79b25-3198-4274-9e58-248dff925548",
    'Host': "api.spotify.com",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

conn.request("GET", "v1,search", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))