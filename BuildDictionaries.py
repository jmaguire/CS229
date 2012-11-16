import os,json
import tldextract


directory = 'RawData/'

dictionary = {}
urls = {}
submitters = {}
dictionaryIndex = 0
urlIndex = 0
submittersIndex = 0

def stripSpace(word):
    while ' ' in word:
        word.replace(' ', '')
    return word

def standardizeWord(word):
    word = str(word)
    trans = ''.join(chr(c) if chr(c).isupper() or chr(c).islower() else '^' for c in range(256))
    word = word.translate(trans)
    word = word.replace('^','')
    word = stripSpace(word)
    return word.lower()

## Add to dict object
## Adds the discovered url/username/word to the relevant dictionary.  
## The key is the stored index. This tells us which value in the overall
## training/test vector to modify. For example word 'hello' might correspond
## to the 517th word in our word vector


def addToUrls(domain):
    global urlIndex
    if domain not in urls:
        urls[domain] = urlIndex;
        urlIndex = urlIndex+1

def addToDictionary(title):
    global dictionaryIndex
    for word in title.split():
        word = standardizeWord(word)
        if len(word) != 0: 
            if word not in dictionary:
                dictionary[word] = dictionaryIndex;
                dictionaryIndex = dictionaryIndex + 1
                
def addToSubmitters(username):
    global submittersIndex
    if username not in submitters:
        submitters[username] = submittersIndex;
        submittersIndex = submittersIndex+1     
        
for dirname, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        path = os.path.join(dirname,filename)
        print path
        path = os.path.abspath(path)
        json_data= open(path).read()
        data = json.loads(json_data)
        posts = data['results'][0]["posts"];
        for post in posts:
            url = post['url'].encode('ascii','ignore')
            domain = tldextract.extract(url)[1].lower()
            title = post['title'].encode('ascii','ignore')
            username = post['submitter'].lower()
            addToSubmitters(username)
            addToDictionary(title)
            addToUrls(domain)

addToSubmitters('unknowncategory')
addToDictionary('unknowncategory')
addToUrls('unknowncategory')

master = {}
master['urls'] = urls
master['dictionary'] = dictionary
master['submitters'] = submitters

data = json.dumps(master)
fp = open('Dictionaries/master.json', 'wb')
json.dump(data, fp)
fp.close()   
