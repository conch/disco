import sys, subprocess

if sys.argv[1] == "install":
  try:
    subprocess.check_output("cp disco_*.py /usr/bin", shell=True)
    print "SUCCESS: DisCo has been installed in /usr/bin"
  except subprocess.CalledProcessError:
    print "ERROR: Could not install DisCo"
elif sys.argv[1] == "uninstall":
  try:
    subprocess.check_output("rm /usr/bin/disco_receiver.py /usr/bin/disco_write_to_sqlite.py", shell=True)
    print "SUCCESS: DisCo has been uninstalled"
  except subprocess.CalledProcessError:
    print "ERROR: Could not uninstall DisCo"
  