import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
url = "http://www.gomaji.com/Taipei"
response = urllib2.urlopen(url)
page_source = response.read()
tmp = page_source.split("<a href=\"/index.php?city=")
Uset = set()
for i in range(1,len(tmp)-1,1):
	Uset.add("http://www.gomaji.com/index.php?city="+tmp[i].split("\"")[0])
for x in Uset:
	if "http" in x:continue
	if "Taipei_" not in x:continue
	print x

def GetInfo(url,Rset):
	response = urllib2.urlopen(url)
	page_source = response.read()
	tmp = page_source.split(".html\" target=\"_blank\"")
	for i in range(0,len(tmp)-1,1):
		tmpp = tmp[i].split("\"")
		Rset.add(tmpp[len(tmpp)-1])
	return Rset

Rset = set()
for x in Uset:
	Rset = GetInfo(x,Rset)

for x in Rset:
	if "Taipei_" not in x:continue
	if "http" not in x:
		print x
