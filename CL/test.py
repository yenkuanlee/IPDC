import control
#import crawler
a = control.Control()
a.DataUpload()
a.SetKRunner(2)
#RunnerList = list(a.Runner)
#b = crawler.Crawler(a.JobID,0,RunnerList)
#b.Run()
a.CallDownload()
a.CallRun()
