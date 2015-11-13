## SPECIFY FILE PATTERN IN QUOTES!!!!
## IT'S IMPORTANT!
import os, time, stat
import argparse
from glob import glob
from itertools import chain

UNKNOWN = 3
CRITICAL = 2
WARNING = 1
OK = 0
parser = argparse.ArgumentParser( )
parser.add_argument("--directory",
                     help="Serch path")
parser.add_argument("--file",
                     help="Search pattern")
parser.add_argument("--log",
                     default="/mnt/logs/outdated-files.log",
                     help="Where to store outdated files")
parser.add_argument("--warning",
                    default=2592000,
                    help="threshold for critical alert e.g. 1000")
parser.add_argument("--critical",
                    default=5184000,
                    help="threshold for critical alert e.g. 1000")
args = parser.parse_args( )

def file_check(warning , critical , directory , file_r , log):
    if not directory:
        directory = r"{}".format(os.path.dirname(os.path.realpath(__file__)))
    pattern = r'{}'.format(file_r)
    chk_crit = [0]
    chk_warn = [0]
    files = [y for x in os.walk(directory) for y in glob(os.path.join(x[0], pattern))]
    log = open(log, 'w')
    for f in files:
        st = os.stat(f)
        mtime = st.st_mtime
        age = int(time.time() - mtime)
        if age > int(critical):
            print >> log, f + " " + "is older than a threshold %s" % args.critical
            chk_crit.extend([1])
        elif age > int(warning):
            print >> log, f + " " + "is in warning state %s" % age
            chk_warn.extend([1])

    if (max(chk_crit) == 1):
        res = 1
    elif (max(chk_warn) == 1):
        res = 0.5
    else:
        res = 0
    return res
    log.close()

def main():
    res = file_check(args.warning,args.critical,args.directory,args.file,args.log)
    if res == 1:
        print "CRITICAL: There are outdated files. Check the application log %s" % args.log
        exit(CRITICAL)
    elif res == 0.5:
        print "WARNING: There are outdated files. Check the application log %s" % args.log
        exit(WARNING)
    elif res == 0:
        print "OK: There are no outdated files."
        exit(OK)

if __name__ == "__main__":
  main( )
