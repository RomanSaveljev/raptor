#
# Copyright (c) 2009-2014 Microsoft Mobile and/or its subsidiary(-ies).
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
# Classes, methods and regex available for use in log filters
#

# This particular file is preliminary and under development.
# The related code is in meta.MetaReader class, and mainly in 
# method "__init__" and "ReadBldInfFiles"
class MetadataPlatform(object):
	""" A metadata platform is a set of configurations which share
	the same metadata. In other words, a set of configurations
	for which the bld.inf and MMP files pre-process to exactly
	the same text."""
	
	def __init__(self, build, config):
		evaluator = build.GetEvaluator(None, config)
		self.selfform= evaluator.CheckedGet("TRADITIONAL_PLATFORM")
		epocroot = evaluator.CheckedGet("EPOCROOT")
		self.epocroot = generic_path.Path(epocroot)
		sbs_build_dir = evaluator.CheckedGet("SBS_BUILD_DIR")
		self.sbs_build_dir = generic_path.Path(sbs_build_dir)
		flm_export_dir = evaluator.CheckedGet("FLM_EXPORT_DIR")
		self.flm_export_dir = generic_path.Path(flm_export_dir)
		self.cacheid = flm_export_dir

		if utilities.getOSPlatform().startswith("win"):
			self.platmacros = evaluator.CheckedGet( "PLATMACROS.WINDOWS")
		else:
			self.platmacros = evaluator.CheckedGet( "PLATMACROS.LINUX")
			
		self.configs = Set()

		# is this a feature variant config or an ordinary variant
		fv = evaluator.Get("FEATUREVARIANTNAME")
		if fv:
			variantHdr = evaluator.CheckedGet("VARIANT_HRH")
			variantHRH = generic_path.Path(variantHdr)
			self.isfeaturevariant = True
		else:
			variantCfg = evaluator.CheckedGet("VARIANT_CFG")
			variantCfg = generic_path.Path(variantCfg)
			if not variantCfg in variantCfgs:
				# get VARIANT_HRH from the variant.cfg file
				varCfg = getVariantCfgDetail(self.epocroot, variantCfg)
				variantCfgs[variantCfg] = varCfg['VARIANT_HRH']
				# we expect to always build ABIv2
				if not 'ENABLE_ABIV2_MODE' in varCfg:
					build.Warn("missing flag ENABLE_ABIV2_MODE in %s file. ABIV1 builds are not supported.",
										   str(variantCfg))
			variantHRH = variantCfgs[variantCfg]
			self.isfeaturevariant = False

			self.variant_hrh = variantHRH
			build.Info("'%s' uses variant hrh file '%s'", config.name, variantHRH)
			self.systeminclude = evaluator.CheckedGet("SYSTEMINCLUDE")
			
			self.target_types = evaluator.CheckedGet("TARGET_TYPES")
			
			# find all the interface names we need
			ifaceTypes = evaluator.CheckedGet("INTERFACE_TYPES")
			self.interfaces = ifaceTypes.split()

			for iface in self.interfaces:
				#detail[iface] = evaluator.CheckedGet("INTERFACE." + iface)
				self.__dict__[iface] = evaluator.CheckedGet("INTERFACE." + iface)

			# not test code unless positively specified
			self.testcode = evaluator.CheckedGet("TESTCODE", "")

			# make a key that identifies this platform uniquely
			# - used to tell us whether we have done the pre-processing
			# we need already using another platform with compatible values.

			key = str(self.variant_hrh) + str(self.epocroot) \
			     + self.systeminclude + self.platform + self.platmacros

			# Keep a short version of the key for use in filenames.
			uniq = hashlib.md5()
			uniq.update(key)

			self.key = key
			self.key_md5 = "p_" + (uniq.encode().hexdigest()).decode()
			del uniq


class ExportPlatform(MetadataPlatform):
	""" Exports are not "platform dependent" but they are configuration
	 dependent because different configs can have different EPOCROOT
	 and VARIANT_HRH values. Each "build platform" has one associated
	 "export platform" but several "build platforms" can be associated
	 with the same "export platform".	 
	 """

	def __init__(self, build, config):
		#MetaDataPlatform.init(self, build, config)
		super(ExportPlatform, self).__init__(build, config)

	def __hash__(self):
		# concatenate all the values we care about in a fixed order
		# and use that as a signature for the exports.
		return  hash(self.epocroot + self.variant_hrh + self.systeminclude + self.testcode + self.export)

	def __eq__(self, other):
		return self.hash() == other.hash()

	@classmethod 
	def fromConfigs(cls, configsToBuild, build):
		
		export_platforms = []
		
		exports = {}

		for config in configsTobuild:
			if export in exports:
				# add this configuration to an existing export platform
				index = exports[export]
				export_platforms[index]['configs'].append(config)
			else:
				# create a new export platform with this configuration
				exports[export] = len(export_platforms)
				exp = copy.copy(detail)
				exp['PLATFORM'] = 'EXPORT'
				exp['configs']  = [config]
				export_platforms.append(exp)

			# compare this configuration to the ones we have already seen

			# Is this an unseen export platform?
			# concatenate all the values we care about in a fixed order
			# and use that as a signature for the exports.
			items = ['EPOCROOT', 'VARIANT_HRH', 'SYSTEMINCLUDE', 'TESTCODE', 'export']
			export = ""
			for i in items:
				if hasattr(cls, i.lower()):
					export += i + str(cls.__dict__[i])

			if export in exports:
				# add this configuration to an existing export platform
				index = exports[export]
				export_platforms[index]['configs'].append(config)
			else:
				# create a new export platform with this configuration
				exports[export] = len(self.ExportPlatforms)
				exp = copy.copy(detail) # need to refactor "detail"
				exp['PLATFORM'] = 'EXPORT'
				exp['configs']  = [config]
				export_platforms.append(exp)
		
		return export_platformss
	


class BldinfPlatform(MetadataPlatform):
	""" Group the list of configurations into "build platforms".
		A build platform is a set of configurations which share
		the same metadata. In other words, a set of configurations
		for which the bld.inf and MMP files pre-process to exactly
		the same text.
	"""
		
	def __init__(self, build, config):
		super(BldinfPlatform, self).__init__(build, config)
		
	def __hash__(self):
		return hash(self.platform) + hash(self.epocroot) + hash(self.variant_hrh) + hash(self.systeminclude) + hash(self.testcode)

	def __cmp__(self, other):
		return cmp(self.hash(), other.hash())

	@classmethod 
	def fromConfigs(cls, configsToBuild, build):
		""" Group the list of configurations into "build platforms".
		"""
		build_platforms = [] # This should replace meta.MetaReader.BuildPlatforms
		               # once the new classes have done.
		platforms = {}
		
		for config in configsToBuild:
			# get everything we need to know about the configuration
			#plat = BldinfPlatform(build, config)

			# Is this an unseen build platform?
			# concatenate all the values we care about in a fixed order
			# and use that as a signature for the platform.
			items = ['PLATFORM', 'EPOCROOT', 'VARIANT_HRH', 'SYSTEMINCLUDE', 'TESTCODE']
			if utilities.getOSPlatform().startswith("win"):
				items.append('PLATMACROS.WINDOWS')
			else:
				items.append('PLATMACROS.LINUX')

			items.extend(cls.interfaces)
			platform = ""
			for i in items:
				#if i in self.__dict__:
				if hasattr(cls, i.lower()):
					platform += i + str(cls.__dict__[i])

			if platform in platforms:
				# add this configuration to an existing build platform
				index = platforms[platform]
				build_platforms[index]['configs'].append(config)
			else:
				# create a new build platform with this configuration
				platforms[platform] = len(build_platforms)
				cls.configs.add()
				build_platforms.append(cls.configs)

		return build_platforms
