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
# Description: sdk module - classes for dealing with SDKs

import os
import xml.sax
import xml.sax.saxutils

class SDKListFromXML(xml.sax.handler.ContentHandler):
	def __init__(self):
		self.sdks = []
		self.in_sdk = False
		self.in_er = False
		self.in_lp = False
		
		self.chars_buffer = ""	
		self.info = None
		self.epocroot = None
		self.logpath = None
	
	def startElement(self, name, attrs):
		if name == "sdk":
			self.info = ""
			self.epocroot = ""
			self.logpath = ""
			self.in_sdk = True
			if "info" in attrs.getNames():
				self.info = str(attrs.getValue("info"))
		
		if self.in_sdk:
			if name == "epocroot":
				self.in_er = True
			if name == "logpath":
				self.in_lp = True
	
	def endElement(self, name):
		if name == "sdk":
			self.in_sdk = False
			self.sdks.append([	xml.sax.saxutils.unescape(self.epocroot),
								xml.sax.saxutils.unescape(self.logpath), 
								xml.sax.saxutils.unescape(self.info, 
									{"&quot;" : "\"", "&apos;" : "'"}) ])
		if name == "epocroot":
			self.in_er = False
		if name == "logpath":
			self.in_lp = False
	
	def characters(self, content):
		if self.in_er:
			self.epocroot += str(content)
		if self.in_lp:
			self.logpath += str(content)

class SDK(object):
	def __init__(self, epocroot, logpath = None, sdkinfo = ''):
		self.epocroot = epocroot
		
		if logpath in [ "", None ]:
			self.logpath = os.path.join(self.epocroot, "epoc32", "build")
		else:
			self.logpath = logpath
		
		self.sdkinfo = sdkinfo
	
	def __repr__(self):
		return "SDK(r'{0}', r'{1}', r'{2}')".format(self.epocroot, self.logpath, self.sdkinfo)
	
	def __str__(self):
		""" Returns an XML representation of the SDK object. """
		return "<sdk info={0}>\n<epocroot>{1}</epocroot>\n<logpath>{2}</logpath>\n</sdk>".format(
						xml.sax.saxutils.quoteattr(self.sdkinfo), 
						xml.sax.saxutils.escape(self.epocroot), 
						xml.sax.saxutils.escape(self.logpath))
	
	def __eq__(self, other):
		"""Enable equality testing between to SDK() objects."""
		return ( (self.epocroot == other.epocroot) and 
				 (self.logpath == other.logpath) and 
				 (self.sdkinfo == other.sdkinfo) ) 

class SdkManager(object):
	"""Manages the list of SDKs available for sbv."""
	
	def __init__(self, config_file = None):
		self.sdk_dict = {}
		if config_file == None: # Use default SDK list
			self.config_file = os.path.expanduser(os.path.join("~", ".sbs_sdk_list.xml"))
		else:
			self.config_file = config_file
		print("Using config file {0}".format(self.config_file))
		
	def __read_sdks(self):
		"""Read the config file and attempt to create an SDK object from the
		repr on each line of this file."""
		
		try:
			sdk_parser  = SDKListFromXML()
			xml.sax.parse(self.config_file, sdk_parser)
		except Exception as e:
			print("Failed to create SDK object from the following line from the SDK list\n" + 
					"{0}\nError was: {1}\n".format(line, e))
			return
		
		current_id = len(self.sdk_dict)
		for sdk_details in sdk_parser.sdks:
			# each sdk_details contains epocroot, logpath and info in that order
			s = SDK(sdk_details[0],
					sdk_details[1],
					sdk_details[2])
			self.sdk_dict[current_id] = s
			current_id = current_id + 1	

	def __write_sdks(self):
		"""Write the SDK's repr to the config_file. The file format is one SDK 
		per line and is the repr of the SDK-class's constructor call. The file is
		overwritten each time this method is called."""
		print("{0} sdk's to save...".format(len(self.sdk_dict)))
		with open(self.config_file, "w") as f:
			f.write("<?xml version=\"1.0\" encoding=\"ISO-8859-1\" ?>\n<sdklist>\n")
			for sdk_id in self.sdk_dict:
				f.write("{0}\n".format(self.sdk_dict[sdk_id]))
			f.write("</sdklist>")
	
	def init_sdk_dict(self):
		"""Return a list of SDK objects suitable for passing to the SDKListModel."""
		if os.path.isfile(self.config_file):
			self.__read_sdks()
		else:
			print("No config file found at {0}. SDK list cannot be initialised.".format(self.config_file))
	
	def add(self, new_sdk):
		""" Add an SDK to the dictionary. Returns the id of the added SDK object. """
		id = len(self.sdk_dict) # 0-based
		self.sdk_dict[id] = new_sdk
		return id
	
	def remove(self, sdk_id):
		""" Remove the SDK whose id is sdk_id """
		try:
			del self.sdk_dict[sdk_id]
			print("Removed SDK with id {0}".format(sdk_id))
		except KeyError as ke:
			print("Unable to remove SDK with id: {0} - no SDK with this id was found.".format(sdk_id))
	
	def shutdown(self):
		"""Writes the SDKs to the config file."""
		self.__write_sdks()
