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
# Filter to generate shell scripts based on a Raptor log
#

import os

from raptor import filter_interface

class ShellScriptsFilter(filter_interface.FilterSAX):
	""" Filter to generate Bash shell scripts.
	This filter takes the following named parameters: "name" and "file"
	"name" specifies the name attribute of a recipe tag to parse for
	"file" specifies a "command file", which has one "name" per line
	
	Recipe names specified in command files come after all recipes specified
	with the filter's "name" parameter, but the order of the recipes in the
	command file is maintained.
	
	E.g.
	
	sbs_filter --filters=ShellScriptsFilter[name=compile,name=linkandpostlink] < a_raptor_log.log
	
	generates the files 
	
	rebuild.sh - calls the shell scripts below in the order given in the filter's parameter list
	compile.sh - contains command from all "compile" recipes
	linkandpostlink.sh - contains commands from "linkandpostlink" recipes
	
	sbs_filter --filters=ShellScriptsFilter[file=recipes.txt] < a_raptor_log.log
	
	recipes.txt has the format
	----------------------
	name=compile
	name=linkandpostlink
	----------------------
	
	generates the files 
	
	rebuild.sh - calls the shell scripts below in the order given in the filter's parameter list
	compile.sh - contains command from all "compile" recipes
	linkandpostlink.sh - contains commands from "linkandpostlink" recipes
		 
	"""
	
	def __init__(self, params = ["name=compile", "name=linkandpostlink"]):
		super(ShellScriptsFilter, self).__init__()
		self.params = params
		self.parseParameters()
		
		# Flags identifying current recipes
		self.want_recipe = False
		self.buffer = "" # Buffer for CDATA
		self.recipe_name = ""
		
		# Open all the shell script files for writing. The file name
		# is the name of the recipe + .sh; existing files are overwritten
		self.recipe_file_dict = {}
		for recipe_name in self.recipe_names:
			self.recipe_file_dict[recipe_name] = { "file" : open(recipe_name + ".sh", "w"), "count" : 0 }
	
	def parseParameters(self):
		parsed_params = self.parseNamedParams(['file', 'name'], self.params)
		self.files = parsed_params['file'] # params that are files
		self.recipe_names = parsed_params['name']  # params that are named
		
		# Get the recipe names from the "command" files if any exist. Each "command" file is 
		# parsed as follows: for each line in the file, remove whitespace from either side; 
		# if the resulting string starts with "name=", grab the substring to the right of the
		# equals sign. This will be added to the list of recipe names. All lines not matching
		# "name=" after being stripped are flagged as warnings.
		for file_name in self.files:
			with open(file_name) as command_file:
				for line in command_file:
					if line.strip().startswith("name="):
						self.recipe_names.append(line.strip()[5:])
					else:
						if line.strip(): # Ignore blank lines or lines containing only whitespace
							print("File {0} contains the unexpected line \"{1}\". " \
								"Lines are expected to start with the string \"name=\".".format(file_name, line.strip()))
		
	def startElement(self, name, attributes):
		"""Handle start element. Here, only look for recipe elements whose "name"
		attribute is in self.recipe_file_dict. If that is the case, the 
		recipe is flagged as wanted and the CDATA buffer self.buffer is reset."""
		if name == "recipe":
			if "name" in attributes.getNames():
				self.recipe_name = attributes.getValue("name")
				
				if self.recipe_name in self.recipe_file_dict:
					 self.buffer = ""
					 self.want_recipe = True
	
	def characters(self, char):
		"""Handles CDATA for a recipe. Append all CDATA to self.buffer only if self.want_recipe is set"""
		if self.want_recipe: 
			self.buffer += char
		
	def endElement(self, name):
		"""Handle end element. If the element is a recipe and the self.want_recipe is set,
		write out the formatted command string from the elements CDATA, increment a counter
		and unset the self.want_recipe flag."""
		if name == "recipe" and self.want_recipe:
			self.recipe_file_dict[self.recipe_name]["file"].write(self.formatCommand(self.buffer))
			self.recipe_file_dict[self.recipe_name]["count"] += 1
			self.want_recipe = False
	
	def endDocument(self):
		print("Summary:")
		for recipe_name in self.recipe_file_dict:
			self.recipe_file_dict[recipe_name]["file"].write("wait\n")
			self.recipe_file_dict[recipe_name]["file"].close()
			print("Recipe name: {0}\tcount:{1}".format(recipe_name, self.recipe_file_dict[recipe_name]["count"]))
		
		# Write overarching shell script
		with open("rebuild.sh", "w") as f:
			for recipe_name in self.recipe_names:
				f.write("bash ./{0}.sh\n".format(recipe_name))
	
	def formatCommand(self, cdata_command_string):
		"""Formats and returns cdata_command_string as a command suitable for running 
		in a Bash shell script. All lines that are not runnable commands are discarded."""
		
		# Split cdata_command_string on new lines, get all the lines that start with a "+ ",
		# which are the ones that Bash has run as command, and remove the "+ ".
		cmd_list = [line[2:] for line in cdata_command_string.split("\n") if line.startswith("+ ")]
		
		# Join the commands with ampersands. If cmd_list contains only one item,
		# " && ".join(cmd_list) simply returns it; append & to the command so that
		# it will be run in the background.
		cmd = "{0} &\n".format(" && ".join(cmd_list))
		return cmd
