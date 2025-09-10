import gui
import gui_prueba
import reportLog

if __name__== "__main__":
    logReport = reportLog.ReportLog()
    logReport.logger.info("Init main")
    gui_prueba.main()
    #gui.main()