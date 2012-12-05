import os,json,tldextract
import csv,random


dir = 'RawData/'


fp = open('master.json', 'r')
data = json.loads(fp.read())
fp.close()
master = json.loads(data)

dictionary = master['dictionary']
urls = master['urls']
submitters = master['submitters']

NORMALIZATION = len(dictionary)


training = []
testing = []

svmTrain = csv.writer(open('SVM_Bayes_Files/TRAIN.csv','wb'))
svmTest = csv.writer(open('SVM_Bayes_Files/TEST.csv','wb'))

trainExamples = csv.writer(open('SVM_Bayes_Files/trainExamples.csv','wb'))
trainClasses = csv.writer(open('SVM_Bayes_Files/trainClasses.csv','wb'))
testExamples = csv.writer(open('SVM_Bayes_Files/testExamples.csv','wb'))
testClasses = csv.writer(open('SVM_Bayes_Files/testClasses.csv','wb'))

def createDictionaryVector(words):
    # Initialize bit vector to zeros
    vector = [0]*len(dictionary)
    # If a word is in the dictionary, increment its
    # index. If the word is not found increment the unknown
    # index
    for word in words:
        index = 0
        if word in dictionary:
            index = dictionary[word]
        else:
            index = dictionary['unknowncategory']
        vector[index] = vector[index] + int(NORMALIZATION/len(vector))
    return vector

def createUsernameVector(username):
    vector = [0]*len(submitters)
    if username in submitters:
        index = submitters[username]
    else:
        index = submitters['unknowncategory']
    vector[index] = vector[index] + int(NORMALIZATION/len(vector))
    return vector

def createURLVector(url):
    vector = [0]*len(urls)
    if url in urls:
        index = urls[url]
    else:
        index = urls['unknowncategory']
    vector[index] = vector[index] + int(NORMALIZATION/len(vector))
    return vector

def createTimeVector(time):
    # Store nearest hour/half hour
    vector = [0]*48
    hour = time[0]
    minute = time[1]
    index = 2*hour+1*(minute > 30)
    vector[index] = vector[index] + int(NORMALIZATION/len(vector))
    return vector

def returnWords(title):
    def standardizeWord(word):
        def stripSpace(word):
            while ' ' in word:
                word.replace(' ', '')
            return word
        word = str(word)
        trans = ''.join(chr(c) if chr(c).isupper() or chr(c).islower() else '^' for c in range(256))
        word = word.translate(trans)
        word = stripSpace(word)
        return word.strip().lower()
    words = []
    for word in title.split():
        word = standardizeWord(word)
        words.append(word)
    return words


def addToTest(title,domain,username,time,points):
    words = returnWords(title)
    dictionaryVector = createDictionaryVector(words)
    usernameVector = createUsernameVector(username)
    urlVector = createURLVector(domain)
    timeVector = createTimeVector(time)
    
    #For naive bayes, the classes, 'y', and the features, 'x', are stored in different
    #files
    testExamples.writerow(dictionaryVector+usernameVector+urlVector+timeVector)
    testClasses.writerow([int(points > 100)])
    
    # For svm, the classes, 'y', make up the first column
    svmTest.writerow([int(points > 100)]+dictionaryVector+usernameVector+urlVector+timeVector)
    
def addToTrain(title,domain,username,time,points):
    words = returnWords(title)
    dictionaryVector = createDictionaryVector(words)
    usernameVector = createUsernameVector(username)
    urlVector = createURLVector(domain)
    timeVector = createTimeVector(time)
    
    #For naive bayes, the classes, 'y', and the features, 'x', are stored in different
    #files
    trainExamples.writerow(dictionaryVector+usernameVector+urlVector+timeVector)
    trainClasses.writerow([int(points > 100)])
    
    # For svm, the classes, 'y', make up the first column
    svmTrain.writerow([int(points > 100)]+dictionaryVector+usernameVector+urlVector+timeVector)
    

# The time that the crawler scraped the site is provided as well as the 
# relative time of the post (For example: '55 minutes ago' or '1 hour ago') 
def getTime(ago,referenceTime):
    # We only care about hours and minutes
    hour = 0 
    minute = 0
    
    if 'minute' in ago:
        minute = int(ago.split('minute')[0])
    if 'hour' in ago:
        hour = int(ago.split('hour')[0])
    
    referenceTime = referenceTime.split('T')[1].split(':')
    referenceMinute = int(referenceTime[1])
    referenceHour = int(referenceTime[0])
    
    minuteCreated = referenceMinute - minute;
    
    # If the minute created is negative, add 60 minutes
    # to the minute value and increase the hours ago field by 1
    if minuteCreated < 0:
        minuteCreated = minuteCreated + 60
        hour = hour + 1
   
    hourCreated = referenceHour - hour;
    
    ##Adjust for events the occurred in the last day 
    if hourCreated < 0:
        hourCreated = hourCreated + 24
        # we don't record day so don't bother to carry over
   
    return hourCreated,minuteCreated

test_count = 0
train_count = 0 
for dirname, dirnames, filenames in os.walk(dir):
    for filename in filenames:
        path = os.path.join(dirname,filename)
        
        print path
        path = os.path.abspath(path)
        json_data= open(path).read()
        data = json.loads(json_data)
        
        posts = data['results'][0]["posts"]
        referenceTime  = data['results'][0]['created_at']
        
        for post in posts:
            
            url = post['url'].encode('ascii','ignore')
            domain = tldextract.extract(url)[1].lower()
            title = post['title'].encode('ascii','ignore')
            username = post['submitter'].lower()
            time = getTime(post['ago'],referenceTime)
            points = post['points']

            if(points > 100 or points < 20):      
                num = random.randint(1,4)
                #train on 75% of the data, test on 25%
                if num == 4:
                    test_count = test_count + 1
                    addToTest(title,domain,username,time,points)
                else:
                    train_count = train_count + 1
                    addToTrain(title,domain,username,time,points)        

print 'done',test_count,train_count
        