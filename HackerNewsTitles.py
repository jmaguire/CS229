import os,json


dir = 'RawData/'

def standardizeWord(word):
    word = str(word)
    trans = ''.join(chr(c) if chr(c).isupper() or chr(c).islower() else '^' for c in range(256))
    word = word.translate(trans)
    word = word.replace('^','')
    return word.replace(' ','').strip().lower()
    


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
            title = post['title']
            title = title.encode('ascii','ignore')
            for word in title.split():
                word = standardizeWord(word)
                if len(word) != 0: 
                    if word in dictionary:
                        dictionary[word] = dictionary[word]+1;
                    else:
                        dictionary[word] = 1
print len(dictionary)
data = json.dumps(dictionary)
fp = open('dictionary.json', 'wb')
json.dump(data, fp)
fp.close()   
print 'done'
                
        