# -*- coding: UTF-8 -*-
# Kevin Yen-Kuan Lee
import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Crawler:
	def __init__(self, JobID, RunnerID, RunnerList):
		self.fw = open('output.txt','w')
                self.JobID = JobID
                self.RunnerID = RunnerID
                self.RunnerList = RunnerList
                self.NumberOfRunner = len(RunnerList)
                self.InputPath = 'data.dat'

                self.RunnerDict = dict()
                for x in self.RunnerList:
                        self.RunnerDict[x[2]] = x[0] # IP
                self.KeyToRunner = dict()

	def crawler(self,info):
		url = ""
		if "http" in info:
			url = info
		else:
			url = "http://www.gomaji.com/"+info+".html"

		response = urllib2.urlopen(url)
		page_source = response.read()
		Cflag = False
		tmp = page_source.split("<script type=\"application/ld+json\">")[1].split("</script>")[0]
		Rdict = dict()
		tmpp = tmp.split("\n")
		for x in tmpp:
			if "\"name\"" in x:
				Rdict['name'] = x.split("\"")[3].split(" - GOMAJI")[0]
			elif "\"productID\"" in x:
				Rdict['productID'] = x.split("\"")[3]
			elif "\"image\"" in x:
				Rdict['image'] = x.split("\"")[3]
			elif "\"description\"" in x:
				Rdict['description'] = x.split("\"")[3]
			elif "\"url\"" in x:
				Rdict['url'] = x.split("\"")[3]
			elif "\"price\"" in x:
				Rdict['price'] = x.split("\"")[3]
		self.fw.write("{\n")
		for x in Rdict:
			self.fw.write(x+" : "+Rdict[x]+"\n")
		self.fw.write("}\n")

	def Run(self):
		self.fw.write("[\n")
		f = open(self.InputPath,'r')
		Lcnt = 0
		while True:
			line = f.readline()
			if not line : break
			line = line.replace("\n","")
			try:
				Runner = Lcnt % self.NumberOfRunner
				Lcnt += 1
				if Runner != self.RunnerID : continue
				self.crawler(line)
			except:
				continue
		self.fw.write("]\n")

