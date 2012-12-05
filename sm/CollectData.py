import time
import csv
import json
from BeautifulSoup import BeautifulSoup
import mechanize
import random

url = 'http://rewindhn.com/api/v1/pages?limit=200'

class HackerNewsMiner():
    def __init__(self):
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
    def getResults(self,pageno,start,end):
        self.url = url+'&spec={"page":'+str(pageno)+',"idx":{"$gte":'+str(start)+',"$lt":'+str(end)+'}}&sort(1)&fields=null'
        page = self.br.open(self.url)
        html = page.read()
        return json.loads(html)
    def saveResults(self,filename,data):
        fp = open(filename+'.json', 'wb')
        json.dump(data, fp)
        fp.close()
if __name__ == "__main__":
    miner = HackerNewsMiner(); 
    data = miner.getResults(0,0,200)
    index = 0;
    while(data['count'] != 0):
        time = data['results'][0]["created_at"];
        time = time.replace(':',';')
        miner.saveResults('RawData/'+time+'__00',data)
        time = data['results'][1]["created_at"];
        time = time.replace(':',';')
        miner.saveResults('RawData/'+time+'__01',data)
        print index;
        index = index + 200;
        data = miner.getResults(0,index,index+200)
        