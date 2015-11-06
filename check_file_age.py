import os, time, stat
import argparse
from glob import glob

UNKNOWN = 3
CRITICAL = 2
WARNING = 1
OK = 0
parser = argparse.ArgumentParser( )
parser.add_argument("--warning",
                    default=3600,
                    help="threshold for warning alert e.g. 500")
parser.add_argument("--critical",
                    default=36000,
                    help="threshold for critical alert e.g. 1000")
args = parser.parse_args( )

def file_check(warning , critical):
    chk_crit = [0]
    chk_warn = [0]
    files = [y for x in os.walk("/Users/yurii.rochniak/Training/") for y in glob(os.path.join(x[0], '*.py'))]
    log = open('log.txt', 'w')
    for f in files:
        st = os.stat(f)
        mtime = st.st_mtime
        age =  int(time.time() - mtime)
        if age > critical:
    #        print "CRITICAL: There are outdated files"
             print >> log, f + " " + "is older than a threshold %s" % args.critical
             chk_crit = chk_crit.extend(1)
        elif age > warning:
    #        print "WARNING: There are outdated files"
             print >> log, f + " " + "is in warning state %s" % age >> log
             chk_warn = chk_warn.extend(1)
        else:
    #        print "OK: There are no outdated files"
             continue
    if (max(chk_crit) == 1):
        res = 1
    elif (max(chk_warn) == 1 and max(chk_crit) == 0):
        res = 0.5
#    elif not (np.all(chk_crit) and np.all(chk_warn) and chk_ok == 1):
#        res = 0
    else:
#        print "Unknown error. Check script"
#        exit(UNKNOWN)a
         res = 0
    print chk_crit
    print chk_warn
    return res
    log.close()
def main():
    res = file_check(args.warning,args.critical)
    if res == 1:
        print "CRITICAL: There are outdated files"
        exit(CRITICAL)
    elif res == 0.5:
        print "WARNING: There are outdated files"
        exit(WARNING)
    elif res == 0:
        print "OK: There are no outdated files"
        exit(OK)

if __name__ == "__main__":
  main( )
