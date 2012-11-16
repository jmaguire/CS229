import os,json
import tldextract


dir = 'RawData/'

dictionary = {}
for dirname, dirnames, filenames in os.walk(dir):
    for filename in filenames:
        path = os.path.join(dirname,filename)
        print path
        path = os.path.abspath(path)
        json_data= open(path).read()
        data = json.loads(json_data)
        posts = data['results'][0]["posts"];
        for post in posts:
            url = post['url']
            url = url.encode('ascii','ignore')
            domain = tldextract.extract(url)[1]
            if domain in dictionary:
                dictionary[domain] = dictionary[domain]+1;
            else:
                dictionary[domain] = 1
exit();
data = json.dumps(dictionary)
fp = open('url.json', 'wb')
json.dump(data, fp)
fp.close()   

                
        