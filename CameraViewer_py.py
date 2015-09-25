#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-
"""
 CameraViewer_py.py
 Kenya Ukai
 2015/9/25
 Lisence : MIT
"""

import sys
import time
import RTC
import OpenRTM_aist

import cv2
import cv2.cv as cv
import numpy
import time

cameraviewer_py_spec = ["implementation_id", "CameraViewer_py", 
		 "type_name",         "CameraViewer_py", 
		 "description",       "CameraViewer written in python", 
		 "version",           "1.0.0", 
		 "vendor",            "Kenya Ukai", 
		 "category",          "basic tool", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]

class CameraViewer_py(OpenRTM_aist.DataFlowComponentBase):
	def __init__(self, manager):
	    OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
	    self._d_camera = RTC.CameraImage(RTC.Time(0,0),0, 0, 0, "", 0.0, [])
	    self._cameraIn = OpenRTM_aist.InPort("camera", self._d_camera)
            self.is_alive = True
            
	def onInitialize(self):
	    self.addInPort("camera",self._cameraIn)
	    return RTC.RTC_OK

        def onFinalize(self):
            self.is_alive = False
            return RTC.RTC_OK
            
	def onActivated(self, ec_id):
	    return RTC.RTC_OK

	def onDeactivated(self, ec_id):
	    return RTC.RTC_OK

	def onExecute(self, ec_id):
            if self._cameraIn.isNew():
                self._d_camera = self._cameraIn.read()
	    return RTC.RTC_OK

        def getImage(self):
            return self._d_camera
        
        def isAlive(self):
            return self.is_alive

        
def CameraViewer_pyInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=cameraviewer_py_spec)
    manager.registerFactory(profile,
                            CameraViewer_py,
                            OpenRTM_aist.Delete)


    
def main():
	manager = OpenRTM_aist.Manager.init(sys.argv)
        manager.activateManager()
        CameraViewer_pyInit(manager)
        comp = manager.createComponent("CameraViewer_py")
	manager.runManager(True)

        print("Press 'esc' on camera window to end.")
        cv2.namedWindow("CameraViewer_py", cv.CV_WINDOW_AUTOSIZE)
        time1 = 0.0
        while comp.isAlive():
            time2 = time.time()
            fps = 1.0 / (time2 - time1)
            time1 = time2
            
            cam_img = comp.getImage()
            if cam_img.height>0 and cam_img.width>0:
                pixels = numpy.array([ord(i) for i in cam_img.pixels], dtype = numpy.uint8)
                pixels = pixels.reshape(cam_img.height, cam_img.width, 3)
                cv2.putText(pixels,"END:ESC |  %d FPS"%fps,(20,20),cv2.FONT_HERSHEY_PLAIN ,1,(255,255,255))
                cv2.imshow("CameraViewer_py",pixels)
            if cv2.waitKey(10) == 27:
                break
        cv2.destroyAllWindows()
        manager.terminate()
        
if __name__ == "__main__":
	main()

