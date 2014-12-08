import re, string, sys 
import os.path

currentdir = os.curdir
settingsfile = os.path.join(currentdir,"settings.py")
configdir = os.path.join(currentdir,"settings_config")
configfile = os.path.join(configdir,sys.argv[1])
basicfile = os.path.join(configdir,"basic")

print "Current directory:",currentdir
print "Settings file:",settingsfile
print "Config file:",configfile
print "Basic file:",basicfile

main = open(settingsfile,"w")
basic = open(basicfile,"r")
basicList = basic.readlines()
main.writelines(basicList)
basic.close()
config = open(configfile,"r")
configList = config.readlines()
main.writelines(configList)
config.close()
main.close()