# tool for ROI selection and saving in 2P excitation profile for Zebrascope
# by Nikita Vladimirov <nvladimus@gmail.com>
# started 08Jan2015
from ij import IJ
from ij.plugin.frame import RoiManager
from java.awt.event import MouseAdapter, KeyEvent, KeyAdapter
from ij.gui import GenericDialog, WaitForUserDialog, GenericDialog, Roi, OvalRoi, Toolbar, Overlay
from ij.io import SaveDialog

def getOptions():
    global listener, xlist, ylist, zlist, manager
    gd = GenericDialog("Target Selection")
    gd.addMessage('Mandatory parameters\n')
    gd.addChoice('type', ['point', 'circle', 'spiral'], 'point')
    gd.addNumericField("                power (%)", 85, 0)
    gd.addNumericField("                duration (millisec)", 3, 0) 
    gd.addNumericField("                interval between entries (ms)", 5000, 0)
    gd.addNumericField("                Z-start of stack (microns)", 0, 0)
    gd.addNumericField("                Z-step of stack (microns)", 5, 0)
    gd.addMessage('Optional\n')
    gd.addNumericField("                radius of a circle/spiral", 5, 0) 
    gd.addNumericField("                num. of turns per circle/spiral", 3, 0)
    gd.addNumericField("                take image after every .. entries", 1, 0)    
    gd.addNumericField("                add offset to X coordinates", 0, 0)
    gd.addNumericField("                add offset to Y coordinates", 0, 0)  
    gd.addNumericField("                imaging stack # for excitation onset (0,1,..)", 0, 0)     
    gd.addMessage('Press ENTER to save the coordinate file\n')
    gd.addMessage('Press ESC to restart\n')
    gd.showDialog()
    profileType = gd.getNextChoice()
    power = gd.getNextNumber()
    duration = gd.getNextNumber() 
    prewait = gd.getNextNumber()
    zStart = gd.getNextNumber()
    zStep = gd.getNextNumber()
    r = gd.getNextNumber()
    Nturns = gd.getNextNumber()
    camTriggerEvery = gd.getNextNumber()
    xOffset = gd.getNextNumber()
    yOffset = gd.getNextNumber()
    tmIndex = gd.getNextNumber()
    if gd.wasCanceled():
        IJ.setTool(Toolbar.RECTANGLE)
        return 
    else: 
        return r, power, profileType, duration, Nturns, camTriggerEvery, zStart, zStep, prewait, xOffset, yOffset, tmIndex

def reset():
    global radius, iROI, power, profileType, duration, Nturns, xlist, ylist, zlist, camTriggerEvery, zStart, zStep, prewait, xOffset, yOffset, tmIndex
    xlist = []
    ylist = []
    zlist = []
    manager.runCommand('Reset')
    manager.runCommand('Show All')
    iROI = 0
    options = getOptions()
    if options is not None:
        radius, power, profileType, duration, Nturns, camTriggerEvery, zStart, zStep, prewait, xOffset, yOffset, tmIndex = options
 
class ML(MouseAdapter):
    def mousePressed(self, keyEvent):
        global iROI, xlist, ylist, zlist
        iROI += 1
        canv = imp.getCanvas()
        p = canv.getCursorLoc()
        z = imp.getCurrentSlice()
        roi = OvalRoi(p.x - radius, p.y - radius, radius*2, radius*2)
        roi.setName('z' + str(z) + 'cell' + str(iROI))
        roi.setPosition(z)
        xlist.append(p.x)
        ylist.append(p.y)
        zlist.append(z)
        imp.setRoi(roi)
        manager.addRoi(roi)
        manager.runCommand('Draw')

class ListenToKey(KeyAdapter):
    def keyPressed(this, event):
        doSomething(event)

def doSomething(keyEvent):
  """ A function to react to key being pressed on an image canvas. """
  global iROI, xlist, ylist, zlist, power, profileType, duration, Nturns, camTriggerEvery, zStart, zStep, prewait, xOffset, yOffset, tmIndex
#  print "clicked keyCode " + str(keyEvent.getKeyCode())
  if keyEvent.getKeyCode() == 10: # Enter is pressed!
      sd = SaveDialog('Save ROIs','.','Eprofile','.txt')
      directory = sd.getDirectory()
      filename = sd.getFileName()
      filepath = directory + filename
      f = open(filepath, 'w')
      f.write('<zStart units="um">' + str(zStart) + '</zStart>\n')
      f.write('<zStep units="um">' + str(zStep) + '</zStep>\n')
      f.write('<xOffset units="px">' + str(xOffset) + '</xOffset>\n')
      f.write('<yOffset units="px">' + str(yOffset) + '</yOffset>\n')
      f.write('<radiusROI units="px">' + str(radius) + '</radiusROI>\n\n')
      for i in range(len(xlist)):
            f.write('#cell num:'+str(i)+'\n')
            f.write('ENTRY_START\n')
#            f.write('ABLATION(OFF,200.0)\n') #never used
            f.write('PRE_WAIT(' + str(prewait)+ ')\n')
            f.write('TM_INDEX(' + str(tmIndex)+ ')\n')
#            f.write('PRE_TRIGGER(OFF,5000,CONTINUE)\n') #never used
            f.write('COORDINATES('+str(xOffset + xlist[i])+','+str(yOffset + ylist[i])+','+str(zStart + (zlist[i]-1)*zStep)+')\n')
            if(profileType == 'point'):
                f.write('SCAN_TYPE(POINT)\n')
            if(profileType == 'circle'):
                f.write('SCAN_TYPE(CIRCLE,'+ str(radius) + ',' + str(round(duration/Nturns)) +')\n')
            if(profileType == 'spiral'):
                f.write('SCAN_TYPE(SPIRAL,' + str(radius) + ',' + str(duration) + ',0,'+str(Nturns)+')\n')     
            f.write('POWER(' + str(power) + ')\n')
            f.write('DURATION(' +str(duration)+')\n')
#            f.write('POST_TRIGGER(OFF,0, CONTINUE)\n') #never used
            f.write('CAMERA_TRIGGER\n')
            f.write('ENTRY_END\n\n')
      f.close()
      manager.runCommand('Save',directory+filename+'.zip')
  if keyEvent.getKeyCode() == 27: # Esc is pressed!
      reset()
  keyEvent.consume()

# MAIN code         
imp = IJ.getImage()
IJ.setTool(Toolbar.RECTANGLE)
manager = RoiManager.getInstance()
if manager is None:
    manager = RoiManager();   
reset()
listener = ML()
keyLis = ListenToKey()
win = imp.getWindow()
win.getCanvas().addMouseListener(listener)
win.getCanvas().addKeyListener(keyLis)



