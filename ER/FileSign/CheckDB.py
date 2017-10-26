import sqlite3
DbPath = "/tmp/.db"
conn = sqlite3.connect(DbPath+"/chain.db")
c = conn.cursor()
AskResource = c.execute("select * from askresource")
print "AskResource : "
for x in AskResource:
	print x

RunningChain = c.execute("select * from RunningChain")
print "RunningChain : "
for x in RunningChain:
	print x
