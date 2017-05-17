import control
a = control.Control()

a.DataUpload()
a.SetKRunner(2)
a.CallDownload()
a.CallMap()

a.CheckResult()
