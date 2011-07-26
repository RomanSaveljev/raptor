#
# -*- coding: utf-8 -*-
# 
# Copyright (c) 2011 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved.
# This component and the accompanying materials are made available
# under the terms of the License "Eclipse Public License v1.0"
# which accompanies this distribution, and is available
# at the URL "http://www.eclipse.org/legal/epl-v10.html".
# 
# Initial Contributors:
# Nokia Corporation - initial contribution.
# 
# Contributors:
# 
# Description:

 
import os
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import QDeclarativeView
from PySide import QtDeclarative
from PySide import QtOpenGL
sys.path.append("..")
import allo.diff
from buildrecord import *
import subprocess
import sdk


class BuildWrapper(QObject):
	""" Present a build in the list in a form that the gui can cope with """
	def __init__(self, thing):
		QObject.__init__(self)
		self._thing = thing
		self._checked = False

	def _name(self):
		return self._thing.name

	def _info(self):
		return self._thing.commandline

	def is_checked(self):
		return self._checked

	def toggle_checked(self):
		self._checked = not self._checked
		self.changed.emit()

	changed = Signal()

	info = Property(unicode, _info, notify=changed)
	name = Property(unicode, _name, notify=changed)
	checked = Property(bool, is_checked, notify=changed)

class SDKWrapper(QObject):
	""" Present a build in the list in a form that the gui can cope with """
	def __init__(self, sdk_id, sdk):
		QObject.__init__(self)
		self._sdk_id = sdk_id
		self._sdk = sdk
		self._checked = False
	
	def _id(self):
		return self._sdk_id

	def _path(self):
		return self._sdk.logpath

	def _info(self):
		return self._sdk.sdkinfo

	def is_checked(self):
		return self._checked

	def toggle_checked(self):
		self._checked = not self._checked
		self.changed.emit()

	changed = Signal()
	
	id = Property(unicode, _id, notify=changed)
	info = Property(unicode, _info, notify=changed)
	path = Property(unicode, _path, notify=changed)
	checked = Property(bool, is_checked, notify=changed)


class SDKListModel(QAbstractListModel):
	COLUMNS = ['sdk']
	DEFAULT_LOCATIONS = {"linux" : [ os.path.expanduser(os.path.join("~", "epocroot", "epoc32")) ],
						 "win" : [ drive + ":\\" for drive in ["D", "E", "X", "Y", "Z"] ]
						 			 }

	def __init__(self):
		QAbstractListModel.__init__(self)
		
		# Initialise the SDK manager and read the SDK list from last time
		self.sdk_manager = sdk.SdkManager()
		self.sdk_manager.init_sdk_dict()
		self.initSdks()
	
	# bool QAbstractItemModel::removeRows ( int row, int count, const QModelIndex & parent = QModelIndex() ) [virtual]
	def removeRows(self, row, count, parent = QModelIndex()):
		# beginRemoveRows ( const QModelIndex & parent, int first, int last ) 
		self.beginRemoveRows(parent, row, row + count - 1)
		
		sdk = self._sdks[row]
		
		self.sdk_manager.remove(sdk.id)
		del self._sdks[row]
		
		self.initSdks()
		self.endRemoveRows()
		
	
	def initSdks(self):
		""" Initialise the list of SDKs for the list model """
		self._sdks = []
		
		if "EPOCROOT" in os.environ:
			er = os.environ["EPOCROOT"]
			logpath = None
			if "SBS_BUILD_DIR" in os.environ:
				logpath = os.environ["SBS_BUILD_DIR"]
			env_er = sdk.SDK(er, logpath)
			
			# Don't add the current environment's EPOCROOT if it's
			# already in the sdk list from before
			if not env_er in self.sdk_manager.sdk_dict.values():
				self.sdk_manager.add(env_er)
		
		guessed_locations = [ loc for k in SDKListModel.DEFAULT_LOCATIONS.keys() if 
				k in sys.platform.lower() for loc in SDKListModel.DEFAULT_LOCATIONS[k] ]
		
		for loc in guessed_locations:
			if os.path.isdir(loc):
				s = sdk.SDK(loc, None, "Discovered SDK at " + loc)
				if not s in self.sdk_manager.sdk_dict.values():
					self.sdk_manager.add(s)
		
		self.setRoleNames(dict(enumerate(SDKListModel.COLUMNS)))
		
		self._sdks.extend([SDKWrapper(sdk_id, self.sdk_manager.sdk_dict[sdk_id]) 
						for sdk_id in self.sdk_manager.sdk_dict])

	def rowCount(self, parent=QModelIndex()):
		return len(self._sdks)

	def checked(self):
		return [x for x in self._sdks if x.checked]

	def data(self, index, role):
		if index.isValid() and role == SDKListModel.COLUMNS.index('sdk'):
			return self._sdks[index.row()]
		return None
	
	def remove(self, sdk_id):
		""" Remove the SDK whose is id sdk_id """
		self.sdk_manager.remove(sdk_id)
		self.initSdks()
	
	def sdk_info(self, sdk_id):
		try:
			requested_sdk = [ sdk for sdk in self._sdks if sdk.id == sdk_id ][0]
			return requested_sdk.info
		except:
			return ""

	changed = Signal()

class BuildListModel(QAbstractListModel):
	COLUMNS = ['build']

	def __init__(self, logpath):
		QAbstractListModel.__init__(self)

		self.setRoleNames(dict(enumerate(BuildListModel.COLUMNS)))
		self._logpath = logpath
		self._builds = self.get_build_items(logpath)

	def newlogpath(self, logpath):
		dir=self._logpath
		try:
			s=os.stat(dir)
		except Exception,e:
			return
		if self._logpath != logpath:
			self._logpath = logpath
			self._builds = self.get_build_items(dir)
			self.changed.emit()

	def rowCount(self, parent=QModelIndex()):
		return len(self._builds)

	def checked(self):
		for x in self._builds:
			if x.checked:
				yield x

	def data(self, index, role):
		if index.isValid() and role == BuildListModel.COLUMNS.index('build'):
			return self._builds[index.row()]
		return None

	def get_build_items(self,dir):
		builds = BuildRecord.all_records(dir,100)
		buildcells = []
		for b in builds:
			b.name=os.path.split(b.logfilename)[-1]
			if b.name.find("_pp") == -1: # no parallel parsing logs (not the greatest way to distinguish them though)
				buildcells.append(BuildWrapper(b))

		return buildcells

	def _getlogpath(self):
		return self._logpath

	changed = Signal()
	logpath  = Property(unicode, _getlogpath, notify=changed)

class BuildController(QObject):
	def __init__(self, app, model, sdk_id, sdk_model):
		QObject.__init__(self)
		self.app = app
		self.model = model
		self._info = ".."
		self.sdk_id = sdk_id
		self.sdk_model = sdk_model
		
		print("self.model = {0}".format(self.model))
		print("self.sdk_model = {0}".format(self.sdk_model))

	@Slot(QObject)
	def toggled(self, wrapper):
		wrapper.toggle_checked()
		br = wrapper._thing

	def _getinfo(self):
		return self._info

	@Slot()
	def filterclean(self):
		pass

	@Slot()
	def filternofailed(self):
		pass
	
	@Slot()
	def unregister(self):
		print("Unregistering the sdk with id {0}".format(self.sdk_id))
		self.sdk_model.remove(self.sdk_id)
	
	@Slot(str)
	def newlogpath(self, logpath):
		self.model.newlogpath(logpath)

	infochanged = Signal()
	info = Property(unicode, _getinfo, notify=infochanged)

class SDKController(QObject):
	def __init__(self, app, model):
		QObject.__init__(self)
		self.app = app
		self.model = model
		self.logviews = []

	@Slot(QObject)
	def toggled(self, wrapper):
		wrapper.toggle_checked()
		self.logviews.append(LogView(self.app, wrapper.path, wrapper.id, self.model, 128))
		
#		selectionModel = self.model.selectionModel()
#		for i in selectionModel.selectedIndexes():
#			print("Selected indices are : {0}".format(i))		
     

	def checked_logs(self):
		for lv in self.logviews:
			for build in lv.checked():
			 	yield build._thing

	@Slot()
	def diff(self):
			logs_to_diff = []
			for b in self.checked_logs():
				print "diffing ", b.logfilename
				logs_to_diff.append(b.logfilename)
				if len(logs_to_diff) > 2:
					break

			# generate the intermediate files which make it possible to compare the builds
			log_a = allo.diff.DiffableLog(logs_to_diff[0])
			log_b = allo.diff.DiffableLog(logs_to_diff[1])

			# now do the comparison
			log_diff = allo.diff.LogDiff(log_a, log_b)

			# the short report. it gives a good idea of how similar the results are
			difftext = ""
			difftext += ("\nComponent differences (if any) ======================================\n")
			for (bldinf, counts) in log_diff.components.items():
				if counts[0] != counts[1]:
					difftext += "{0:>8} {1:<8} {2}\n".format(counts[0], counts[1], bldinf)

			difftext += "\nOverall totals ======================================================\n"
			for (event, counts) in log_diff.events.items():
				difftext += "{0:>8} {1:<8} {2}\n".format(counts[0], counts[1], event)


			# take the detailed diff and create diff_left.txt and diff_right.txt
			# which should be manageable by a graphical diff tool. we trim the size
			# by replacing blocks of matching lines with "== block 1", "== block 2" etc.
			different = log_diff.dump_to_files("diff_left.txt", "diff_right.txt")
			self.dv = DiffView(self.app, difftext,"diff_left.txt", "diff_right.txt")

		
		# update the output
		#self._info =
		#self.infochanged.emit()

	@Slot()
	def quit(self):
		print("Quit called...")
		self.model.sdk_manager.shutdown()
		self.app.quit()

	@Slot(str, str, str)
	def add_sdk(self, info, epocroot, logpath):
		print("Going to add a new SDK...")
		print("New SDK:\ninfo:\"{0}\", epocroot: {1}, logpath: {2}".format(info, epocroot, logpath))
		if logpath == "":
			logpath = os.path.join(epocroot, "epoc32", "build")
		s = sdk.SDK(epocroot, logpath, info)
		print("New SDK {0} added to SDK manager".format(s))
		id = self.model.sdk_manager.add(s)
		self.model._sdks.append( SDKWrapper(id, self.model.sdk_manager.sdk_dict[id]) )
		print("New SDK {0} added to SDK List Model.".format(s))



class SDKView(QObject):
	def __init__(self, app, window, logpath=None):
		QObject.__init__(self)
		self.app = app
		
		self.sdk_list_model = SDKListModel()
		self.controller = SDKController(app, self.sdk_list_model)

		self.view = QDeclarativeView()
		self.glw = QtOpenGL.QGLWidget()
		self.view.setViewport(self.glw)
		self.view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
		window.setCentralWidget(self.view)
		self.rc = self.view.rootContext()
		self.rc.setContextProperty('sdk_controller', self.controller)
		self.rc.setContextProperty('pySDKListModel', self.sdk_list_model)
		self.view.setSource('sdkchooser.qml')
	
	@Slot()
	def quit(self):
		self.controller.quit()
		

class DiffView(QObject):
	def __init__(self, app, difftext, leftfile, rightfile):
		QObject.__init__(self)
		self.app = app


		self.difftext=difftext
		self.window = QMainWindow()
		self.window.setWindowTitle("Log Diffs")

		self.leftfile = leftfile
		self.rightfile = rightfile

		self.view = QDeclarativeView()
		self.glw = QtOpenGL.QGLWidget()
		self.view.setViewport(self.glw)
		self.view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
		self.window.setCentralWidget(self.view)
		self.rc = self.view.rootContext()
		self.rc.setContextProperty('controller', self)
		self.rc.setContextProperty('difftext', self.difftext)
		self.view.setSource('diffview.qml')
		self.window.show()

	@Slot()
	def diff_viewer(self):
		p = subprocess.Popen("gvim -d {0} {1}".format(self.leftfile,self.rightfile), shell=True)
		sts = os.waitpid(p.pid, 0)[1]

	def checked(self):
		for build in self.build_list.checked(): 
				yield build

class LogView(QObject):
	def __init__(self, app, logpath, id, sdk_model, row_number):
		QObject.__init__(self)
		self.app = app
		self.logpath=logpath
		
		self.window = QMainWindow()
		self.window.setWindowTitle("Raptor build viewer")
		self.build_list = BuildListModel(self.logpath)
		self.controller = BuildController(app, self.build_list, id, sdk_model)

		self.view = QDeclarativeView()
		self.glw = QtOpenGL.QGLWidget()
		self.view.setViewport(self.glw)
		self.view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
		self.window.setCentralWidget(self.view)
		self.rc = self.view.rootContext()
		self.rc.setContextProperty('controller', self.controller)
		self.rc.setContextProperty('pyBuildListModel', self.build_list)
		self.rc.setContextProperty('logpath', self.logpath)
		self.rc.setContextProperty('info', sdk_model.sdk_info(id))
		self.rc.setContextProperty('window', self.window)
		self.rc.setContextProperty('row', row_number)
		self.view.setSource('logchooser.qml')
		self.window.show()

	def checked(self):
		for build in self.build_list.checked(): 
			yield build
			

app = QApplication(sys.argv)
sdkwin = QMainWindow()
sbv = SDKView(app, window = sdkwin)
sdkwin.show()
app.connect( app, SIGNAL("lastWindowClosed()"), sbv, SLOT( "quit()" ) )

# Enter Qt main loop
sys.exit(app.exec_())
