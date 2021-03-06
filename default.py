import xbmc
import xbmcaddon
from subprocess import Popen, PIPE

__settings__   = xbmcaddon.Addon(id="script.service.dlmanager")

class Screensaver(xbmc.Monitor) :
    print("DLMGR: Checking PlayBackState")

    def __init__ (self):
        xbmc.Monitor.__init__(self)
        
    def onScreensaverDeactivated(self):
        print("DLMGR: XBMC in use")
        sick_cmd = "echo " + __settings__.getSetting("sudo_pass") + " | sudo /etc/init.d/sickbeard stop" #stops the sickbeard service
        p = Popen(sick_cmd , shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        print("DLMGR: sickbeard stop: ",out.rstrip(), err.rstrip())
        trans_cmd = __settings__.getSetting("trans_path") + 'transmission-remote --auth=' + __settings__.getSetting("trans_username") + ':' + __settings__.getSetting("trans_password") + ' -as' # the command line to put transmission into speed limited mode
        p = Popen(trans_cmd , shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        print("DLMGR: transmission throttle: ",out.rstrip(), err.rstrip())
        xbmc.executebuiltin("Notification(Download Manager,Sickbeard stopped. Transmission throttled.)")

    def onScreensaverActivated(self):
        print("DLMGR: XBMC in Standby")
        sick_cmd = "echo " + __settings__.getSetting("sudo_pass") + " | sudo /etc/init.d/sickbeard start" #starts the sickbeard service
        p = Popen(sick_cmd , shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        print("DLMGR: sickbeard start: ",out.rstrip(), err.rstrip())
        trans_cmd = __settings__.getSetting("trans_path") + 'transmission-remote --auth=' + __settings__.getSetting("trans_username") + ':' + __settings__.getSetting("trans_password") + ' -AS' # the command line to disable transmission speed limited mode
        p = Popen(trans_cmd , shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        print("DLMGR: transmission unthrottle: ",out.rstrip(), err.rstrip())

    def onAbortRequested(self):
        print("DLMGR: XBMC is closing")
        sick_cmd = "echo " + __settings__.getSetting("sudo_pass") + " | sudo /etc/init.d/sickbeard start" #starts the sickbeard service
        p = Popen(sick_cmd , shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        print("DLMGR: sickbeard start: ",out.rstrip(), err.rstrip())
        trans_cmd = __settings__.getSetting("trans_path") + 'transmission-remote --auth=' + __settings__.getSetting("trans_username") + ':' + __settings__.getSetting("trans_password") + ' -AS' # the command line to disable transmission speed limited mode
        p = Popen(trans_cmd , shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        print("DLMGR: transmission unthrottle: ",out.rstrip(), err.rstrip())

print("DLMGR: Download Manager Script Loaded")

monitor=Screensaver()

while not xbmc.abortRequested: #End if XBMC closes
    xbmc.sleep(5000) #Repeat (ms) 
