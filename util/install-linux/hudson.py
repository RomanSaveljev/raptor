
# hudson runs this from the raptor/util/install-linux directory

import datetime
import subprocess
import sys

# run "hg id" to get the current branch's tip changeset

hgid = subprocess.Popen(["hg", "id"], stdout=subprocess.PIPE)
stdout = hgid.communicate()[0]

if hgid.returncode == 0 and len(stdout) >= 12:
	changeset = stdout[0:12]
	print "CHANGESET", changeset
else:
	sys.stderr.write("error: failed to get tip mercurial changeset.\n")
	sys.exit(1)

# get today's date in ISO format YYYY-MM-DD

today = datetime.date.today().isoformat()
print "DATE", today

# insert the date and changeset into the raptor_version.py file

filename = "../../python/raptor_version.py"
lines = []
try:
	file = open(filename, "r")
	for line in file.readlines():
		if "ISODATE" in line and "CHANGESET" in line:
			line = line.replace("ISODATE", today)
			line = line.replace("CHANGESET", changeset)
			lines.append(line)
		else:
			lines.append(line)
except IOError, ex:
	sys.stderr.write("error: failed to read file '%s'\n%s" % (filename, str(ex)))
	sys.exit(1)
finally:
	file.close()

# ... and write the modified raptor_version.py file

try:
	#file = open(filename, "w")
	for line in lines:
		sys.stdout.write(line)
except IOError, ex:
	sys.stderr.write("error: failed to write file '%s'\n%s" % (filename, str(ex)))
	sys.exit(1)
finally:
	pass #file.close()

# check the raptor version string

sbs_v = subprocess.Popen(["../../bin/sbs", "-v"], stdout=subprocess.PIPE)
version = sbs_v.communicate()[0]

if sbs_v.returncode == 0:
	print "VERSION", version
	if not today in version or not changeset in version:
		sys.stderr.write("error: date or changeset does not match the sbs version.\n")
		sys.exit(1)
else:
	sys.stderr.write("error: failed to get sbs version.\n")
	sys.exit(1)

