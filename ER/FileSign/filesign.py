import control
import getpass
import sys
a = control.Control()

if sys.argv[1] == "account":
	if sys.argv[2] == "new":
		user = raw_input("Enter user account : ")
		pwd = getpass.getpass()
		a.AccountNew(user,pwd)
	elif sys.argv[2] == "ehash":
		user = raw_input("Enter user account : ")
		ehash = a.GetEhash(user)
		print("Ehash : "+ehash)
elif sys.argv[1] == "file":
	if sys.argv[2] == "upload":
		fname = raw_input("Enter file name : ")
		fhash = a.FileUpload(fname)
		print("File Hash : "+fhash)
	elif sys.argv[2] == "download":
		user = raw_input("Enter user account : ")
		a.FileDownload(user,user+".txt")
	elif sys.argv[2] == "sign":
		user = raw_input("Enter user account : ")
                pwd = getpass.getpass()
		fname = raw_input("Enter file name : ")
		SignHash = a.FileSign(user,pwd,fname)
		print("Sign Hash : "+SignHash)
	elif sys.argv[2] == "send":
		sender = raw_input("Enter sender account : ")
		pwd = getpass.getpass()
		reciver = raw_input("Enter reciver account : ")
		fname = raw_input("Enter file name : ")
		Thash = a.SendFile(sender,pwd,fname,reciver)
		print("Transaction Hash : "+Thash)
elif sys.argv[1] == "varify":
	sender = raw_input("Enter sender account : ")
        pwd = getpass.getpass()
        reciver = raw_input("Enter reciver account : ")
        fname = raw_input("Enter file name : ")
	result = a.Varify(sender,pwd,reciver,fname)
	print("Result : "+str(result))
#a.AccountNew('kevin2','123')
#print a.GetEhash('kevin2')
#print a.FileUpload('test.txt')
#print a.FileSign('kevin','123','test.txt')
#print a.SendFile('admin','123','test.txt','kevin')
#a.GetTransaction("0xcbb7d3f3d6c3db7d0cf1468d81fe3e31ad81113da96baecbfd512946b56df782")
#print a.Varify("admin","123","kevin3","test.txt")
