import os,json
import tldextract

NUM_PAGES = 10

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
    if domain not in urls:
        urls[domain] = 1
    else: 
        urls[domain] = urls[domain]+1

def addToDictionary(title):
    for word in title.split():
        word = standardizeWord(word)
        if len(word) != 0: 
            if word in stopwords:
                continue
            if word not in dictionary:
                dictionary[word] = 1
            else:
                dictionary[word] = dictionary[word] + 1

                
def addToSubmitters(username):
    global submittersIndex
    if username not in submitters:
        submitters[username] = submittersIndex;
        submittersIndex = submittersIndex+1     

stopwords = ['all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having', 'once']

def trimdict():
    index = 0
    for word in dictionary.keys():
        if dictionary[word] < 5:
            del(dictionary[word])
        else:
            dictionary[word] = index
            index = index + 1
    dictionary['unknowncategory'] = index
    dictionary['stopword'] = index+1

def trimurls():
    index = 0
    for word in urls.keys():
        if urls[word] < 5:
            del(urls[word])
        else:
            urls[word] = index
            index = index + 1
    urls['unknowncategory'] = index
        
        
for dirname, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        path = os.path.join(dirname,filename)
        print path
        path = os.path.abspath(path)
        json_data= open(path).read()
        data = json.loads(json_data)
        pages = data['results']
        pagecount = 0
        for page in pages:

            pagecount = pagecount+1;
            if pagecount > NUM_PAGES:
                break   
         
            posts = page['posts']
            for post in posts:
                url = post['url'].encode('ascii','ignore')
                domain = tldextract.extract(url)[1].lower()
                title = post['title'].encode('ascii','ignore')
                username = post['submitter'].lower()
                #     addToSubmitters(username)
                addToDictionary(title)
                addToUrls(domain)

trimdict()
trimurls()

master = {}
master['urls'] = urls
master['dictionary'] = dictionary
#master['submitters'] = submitters

data = json.dumps(master)
fp = open('Dictionaries/master.json', 'wb')
json.dump(data, fp)
fp.close()   
