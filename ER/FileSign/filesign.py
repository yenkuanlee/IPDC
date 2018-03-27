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
