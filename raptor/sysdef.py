#
# Copyright (c) 2007-2014 Microsoft Mobile and/or its subsidiary(-ies).
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
# raptor_sysdef module
#

import os
import re
import xml.dom.minidom

from raptor import generic_path

class SystemModelComponent(generic_path.Path):
	"""Path sub-class that wraps up a component bld.inf file with
	system_definition.xml context information."""

	def __init__(self, aBldInfFile, aLayerName, aContainerNames, aSystemDefinitionFile, aSystemDefinitionBase, aSystemDefinitionVersion):
		generic_path.Path.__init__(self, aBldInfFile.Absolute().path)
		self.__ContainerNames = aContainerNames
		self.__LayerName = aLayerName
		self.__SystemDefinitionFile = aSystemDefinitionFile
		self.__SystemDefinitionBase = aSystemDefinitionBase
		self.__SystemDefinitionVersion = aSystemDefinitionVersion

	def GetSystemDefinitionFile(self):
		return self.__SystemDefinitionFile

	def GetSystemDefinitionBase(self):
		return self.__SystemDefinitionBase

	def GetSystemDefinitionVersion(self):
		return self.__SystemDefinitionVersion

	def GetLayerName(self):
		return self.__LayerName

	def GetContainerName(self, aContainerType):
		if aContainerType in self.__ContainerNames:
			return self.__ContainerNames[aContainerType]
		return ""


class SystemModel(object):
	"""A representation of the SystemModel section of a Symbian system_definition.xml file."""

	def __init__(self, aLogger, aSystemDefinitionFile = None, aSystemDefinitionBase = None, aDoRead = True):
		self.__Logger = aLogger

		if aSystemDefinitionFile:
			self.__SystemDefinitionFile = aSystemDefinitionFile.GetLocalString()
		else:
			self.__SystemDefinitionFile = generic_path.Path('undefined').GetLocalString()

		if aSystemDefinitionBase:
			self.__SystemDefinitionBase = aSystemDefinitionBase.GetLocalString()
		else:
			self.__SystemDefinitionBase = generic_path.Path('undefined').GetLocalString()

		self.__Version = {'MAJOR':0,'MID':0,'MINOR':0}
		self.__IdAttribute = "name"
		self.__ComponentRoot = ""
		self.__TotalComponents = 0
		self.__LayerList = []
		self.__LayerDetails = {}
		self.__MissingBldInfs = {}

		self.__DOM = None
		self.__SystemDefinitionElement = None

		if aDoRead:
			if self.__Read():
				if self.__Validate():
					self.__Parse()

			if self.__DOM:
				self.__DOM.unlink()

	def HasLayer(self, aLayer):
		return aLayer in self.__LayerList

	def GetLayerNames(self):
		return self.__LayerList

	def AddLayer(self, layer):
		"""Add a layer with components to this system definition"""

		for c in layer.children:
			# c.layername takes precedence over layer.name; but if 
			# either is blank, use the non-blank one.
			self.AddComponent(c, c.layername or layer.name)

	def AddComponent(self, aComponent, layername):
		'''Add a dummy component, sufficient for the purposes of
		writing a new system definition file. Argument is a Raptor
		Component object.
		'''
		if layername == '':
			raise Exception("Can't add a component ({0}) without a layer name"
                                        " to a system defintion file".format(str(aComponent.bldinf_filename)))

		containers = {'layer':layername,'component':aComponent.name}
		component = SystemModelComponent(aComponent.bldinf_filename, layername, containers, self.__SystemDefinitionFile, self.__SystemDefinitionBase, self.__Version)

		if not layername in self.__LayerList:
			self.__LayerList.append(layername)

		if layername not in self.__LayerDetails:
			self.__LayerDetails[layername] = []
		self.__LayerDetails[layername].append(component)

	def GetLayerComponents(self, aLayer):
		if not self.HasLayer(aLayer):
			self.__Logger.Error("System Definition layer \"{0}\" does not exist in {1}".format(aLayer, self.__SystemDefinitionFile))
			return []

		return self.__LayerDetails[aLayer]

	def IsLayerBuildable(self, aLayer):
		if aLayer in self.__MissingBldInfs:
			for missingbldinf in self.__MissingBldInfs[aLayer]:
				self.__Logger.Error("System Definition layer \"{0}\""
                                                    " from system definition file \"{1}\""
                                                    " refers to non existent bld.inf file {2}".format(aLayer, self.__SystemDefinitionFile, missingbldinf))

		if len(self.GetLayerComponents(aLayer)):
			return True
		return False


	def GetAllComponents(self):
		components = []

		for layer in self.GetLayerNames():
			components.extend(self.GetLayerComponents(layer))

		return components
	def DumpLayerInfo(self, aLayer):
		if self.HasLayer(aLayer):
			self.__Logger.Info("Found {0} bld.inf references in layer \"{1}\"".format(len(self.GetLayerComponents(aLayer)), aLayer))

	def DumpInfo(self):
		self.__Logger.Info("Found {0} bld.inf references in {1} within {2} layers:".format(len(self.GetAllComponents()), self.__SystemDefinitionFile, len(self.GetLayerNames())))
		self.__Logger.Info("\t{0}".format(", ".join(self.GetLayerNames())))
		self.__Logger.InfoDiscovery(object_type = "layers",
				count = len(self.GetLayerNames()))
		self.__Logger.InfoDiscovery(object_type = "bld.inf references",
				count = len(self.GetAllComponents()))
		
	def Write(self, aFilename):
		"""Write out a system definition that can be used to create an
		identical SystemModel object.
		Note it isn't guaranteed to be a valid system definition - just one
		that will unserialise to an object identical to this one
		"""
		impl = xml.dom.minidom.getDOMImplementation()
		self.__DOM = impl.createDocument(None, "SystemDefinition", None)
		self.__SystemDefinitionElement = self.__DOM.documentElement
		self.__DOM.insertBefore(self.__DOM.createComment('This document is generated by Raptor.  Please do not edit.'),self.__SystemDefinitionElement)
		self.__SystemDefinitionElement.setAttribute('name','MCL')
		self.__SystemDefinitionElement.setAttribute('schema','2.0.0')
		systemModelNode = self.__DOM.createElement('systemModel')
		self.__SystemDefinitionElement.appendChild(systemModelNode)
		for layer in self.__LayerList:
			if len(self.__LayerDetails[layer]) == 0:
				continue
			if layer == '':
				self.__Logger.Error("Can't write out layer with no name to "+aFilename)
			else:
				layerNode = self.__DOM.createElement('layer')
				layerNode.setAttribute('name',layer)
				systemModelNode.appendChild(layerNode)
				for component in self.__LayerDetails[layer]:
					componentNode = self.__DOM.createElement('component')
					componentNode.setAttribute('name',component.GetContainerName('component'))
					layerNode.appendChild(componentNode)
					path = str(component)
					unitNode = self.__DOM.createElement('unit')
					unitNode.setAttribute('bldFile',path)
					componentNode.appendChild(unitNode)
		
		# Record that we haven't stripped the file names off our bld.infs
		self.__SystemDefinitionElement.setAttribute('fullbldinfs','True')

		# Write the sysdef file.  "with" ensures we don't forget to close it.
		with open(aFilename,"w") as f:
			self.__DOM.writexml(f,newl="\n",indent="",addindent="\t")

		self.__DOM.unlink()		

	def __Read(self):
		if not os.path.exists(self.__SystemDefinitionFile):
			self.__Logger.Error("System Definition file {0} does not exist".format(self.__SystemDefinitionFile))
			return False

		self.__Logger.Info("System Definition file {0}".format(self.__SystemDefinitionFile))

		# try to read the XML file
		try:
			self.__DOM = xml.dom.minidom.parse(self.__SystemDefinitionFile)

		except Exception as e: # a whole bag of exceptions can be raised here
			self.__Logger.Error("Failed to parse XML file {0}: {1}".format(self.__SystemDefinitionFile,str(e)))
			return False

		# <SystemDefinition> is always the root element
		self.__SystemDefinitionElement = self.__DOM.documentElement

		return True

	def __Validate(self):
		# account for different schema versions in processing
		# old format : version >= 1.3.0
		# new format : version >= 2.0.0 (assume later versions are compatible...at least for now)
		version = re.match(r'(?P<MAJOR>\d)\.(?P<MID>\d)(\.(?P<MINOR>\d))?', self.__SystemDefinitionElement.getAttribute("schema"))

		if not version:
			self.__Logger.Error("Cannot determine schema version of XML file {0}".format(self.__SystemDefinitionFile))
			return False

		self.__Version['MAJOR'] = int(version.group('MAJOR'))
		self.__Version['MID'] = int(version.group('MID'))
		self.__Version['MINOR'] = int(version.group('MINOR'))

		self.__fullbldinfs = None
		if self.__SystemDefinitionElement.hasAttribute('fullbldinfs'):
			# Lower case it since we're not evil
			if self.__SystemDefinitionElement.getAttribute('fullbldinfs').lower() == 'true':
				self.__fullbldinfs = 1

		if self.__Version['MAJOR'] == 1 and self.__Version['MID'] > 2:
			self.__ComponentRoot = self.__SystemDefinitionBase
		elif self.__Version['MAJOR'] == 2 or self.__Version['MAJOR'] == 3:
			# 2.0.x and 3.0.0 formats support SOURCEROOT or SRCROOT as an environment specified base - we respect this, unless
			# explicitly overridden on the command line
			if 'SRCROOT' in os.environ:
				self.__ComponentRoot = generic_path.Path(os.environ['SRCROOT'])
			elif 'SOURCEROOT' in os.environ:
				self.__ComponentRoot = generic_path.Path(os.environ['SOURCEROOT'])

			if self.__SystemDefinitionBase and self.__SystemDefinitionBase != ".":
				self.__ComponentRoot = self.__SystemDefinitionBase
				if 'SRCROOT' in os.environ:
					self.__Logger.Info("Command line specified System Definition file base \'{0}\'"
                                                           " overriding environment SRCROOT \'{1}\'".format(self.__SystemDefinitionBase, os.environ['SRCROOT']))
				elif 'SOURCEROOT' in os.environ:
					self.__Logger.Info("Command line specified System Definition file base \'{0}\'"
                                                           " overriding environment SOURCEROOT \'{1}\'".format(self.__SystemDefinitionBase, os.environ['SOURCEROOT']))
		else:
			self.__Logger.Error("Cannot process schema version {0} of file {1}".format(version.string, self.__SystemDefinitionFile))
			return False

		if self.__Version['MAJOR'] >= 3:
			# id is the unique identifier for 3.0 and later schema
			self.__IdAttribute = "id"

		return True

	def __Parse(self):
		# For 2.0 and earlier: find the <systemModel> element (there can be 0 or 1) and search any <layer> elements for <unit> elements with "bldFile" attributes
		# the <layer> context of captured "bldFile" attributes is recorded as we go
		# For 3.0 and later, process any architectural topmost element, use the topmost element with an id as the "layer"
		for child in self.__SystemDefinitionElement.childNodes:
			if child.localName in ["systemModel", "layer", "package", "collection", "component"]:
				self.__ProcessSystemModelElement(child)

	def __CreateComponent(self, aBldInfFile, aUnitElement):
		# take a resolved bld.inf file and associated <unit/> element and returns a populated Component object
		containers = {}
		self.__GetElementContainers(aUnitElement, containers)
		layer = self.__GetEffectiveLayer(aUnitElement)
		component = SystemModelComponent(aBldInfFile, layer, containers, self.__SystemDefinitionFile, self.__SystemDefinitionBase, self.__Version)

		return component

	def __GetEffectiveLayer(self, aElement):
		# return layer ID in effect for this unit.  This is either the ID of a parent
		# element called 'layer' or the ID of the first parent whose own parent does
		# not have an ID.  For a well formed v1.x or 2.x system definition these two
		# criteria must point to the same element's ID.  A well formed v3.x system
		# definition does not need a 'layer' component necessarily.
		# Never call this on the root element

		if aElement.tagName == "layer" and aElement.hasAttribute(self.__IdAttribute):
			# Note if we encounter an element named 'layer' before we reach the end
			# of the id stack, we'll use that.
			return aElement.getAttribute(self.__IdAttribute)
		elif aElement.parentNode.hasAttribute(self.__IdAttribute):
			return self.__GetEffectiveLayer(aElement.parentNode)
		elif aElement.hasAttribute(self.__IdAttribute):
			# Note that if we encounter the end of the id stack before we encounter
			# an element called 'layer', we'll use that regardless of whether there's
			# a 'layer' element further up.
			return aElement.getAttribute(self.__IdAttribute)
		return ""

	def __GetElementContainers(self, aElement, aContainers):
		# take a <unit/> element and creates a type->name dictionary of all of its parent containers
		# We're only interested in parent nodes if they're not the top-most node
		if aElement.parentNode.parentNode:
			parent = aElement.parentNode
			name = parent.getAttribute(self.__IdAttribute)

			if name:
				aContainers[parent.tagName] = name

			self.__GetElementContainers(parent, aContainers)

	def __ProcessSystemModelMetaElement(self, aElement):
		# stub method - may deal with metadata elements at some point in the future
		return

	def __ProcessSystemModelElement(self, aElement):
		"""Search for XML <unit/> elements with 'bldFile' attributes and resolve concrete bld.inf locations
		with an appreciation of different schema versions."""

		# Metadata elements are processed separately - there are no further child nodes
		# to process in this context
		if aElement.tagName == "meta" :
			return self.__ProcessSystemModelMetaElement(aElement)

		# The effective "layer" is the item whose parent does not have an id (or name in 2.x and earlier)
		if not aElement.parentNode.hasAttribute(self.__IdAttribute) :
			currentLayer = aElement.getAttribute(self.__IdAttribute)

			if currentLayer not in self.__LayerDetails:
				self.__LayerDetails[currentLayer] = []

			if not currentLayer in self.__LayerList:
				self.__LayerList.append(currentLayer)

		elif aElement.tagName == "unit" and aElement.hasAttributes():
			bldFileValue = aElement.getAttribute("bldFile")

			if bldFileValue:
				bldInfRoot = self.__ComponentRoot

				if self.__Version['MAJOR'] == 1:
					# version 1.x schema paths can use DOS slashes
					bldFileValue = bldFileValue.replace('\\', '/')
				elif self.__Version['MAJOR'] >= 2:
					# version 2.x.x schema paths are subject to a "root" attribute off-set, if it exists
					rootValue = aElement.getAttribute("root")

					if rootValue:
						if rootValue in os.environ:
							bldInfRoot = generic_path.Path(os.environ[rootValue])
						else:
							# Assume that this is an error i.e. don't attempt to resolve in relation to SOURCEROOT
							bldInfRoot = None
							self.__Logger.Error("Cannot resolve \'root\' attribute value \"{0}\" in {1}".format(rootValue, self.__SystemDefinitionFile))
							return

				bldinfval = generic_path.Path(bldFileValue)

				if self.__Version['MAJOR'] < 3:
					# absolute paths are not changed by root var in 1.x and 2.x
					if not bldinfval.isAbsolute() and bldInfRoot:
						bldinfval = generic_path.Join(bldInfRoot, bldinfval)
				else:
					# relative paths for v3
					if not bldinfval.isAbsolute():
						bldinfval = generic_path.Join(generic_path.Join(self.__SystemDefinitionFile).Dir(),bldinfval)
					# absolute paths for v3
					# are relative to bldInfRoot if set, or relative to the drive root otherwise
					elif bldInfRoot:
						bldinfval = generic_path.Join(bldInfRoot, bldinfval)
				
				if self.__fullbldinfs:
					bldinf = bldinfval.FindCaseless()
				else:
					bldinf = generic_path.Join(bldinfval, "bld.inf").FindCaseless()

				if bldinf == None:
					# recording layers containing non existent bld.infs
					bldinfname = bldinfval.GetLocalString()
					if not self.__fullbldinfs:
						bldinfname = bldinfname+'/'+'bld.inf'
					layer = self.__GetEffectiveLayer(aElement)
					if not layer in self.__MissingBldInfs:
						self.__MissingBldInfs[layer]=[]
					self.__MissingBldInfs[layer].append(bldinfname)

				else:
					component = self.__CreateComponent(bldinf, aElement)
					layer = component.GetLayerName()
					if layer:
						self.__LayerDetails[layer].append(component)
						self.__TotalComponents += 1
					else:
						self.__Logger.Error("No containing layer found for {0} in {1}".format(str(bldinf), self.__SystemDefinitionFile))

		# search the sub-elements
		for child in aElement.childNodes:
			if child.nodeType == child.ELEMENT_NODE:
				self.__ProcessSystemModelElement(child)


# end of the sysdef module
