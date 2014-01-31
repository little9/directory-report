#!/usr/bin/env python

# This script generates a report that provides information about files on the archive server


import sys
from subprocess import Popen, PIPE

def gen_directory_report(path):
    data = []
    directory_usage = Popen(["du", "-h", path], stdout=PIPE).communicate()[0]
    directory_usage_list = [s.strip().split('\t') for s in directory_usage.splitlines()]
    for i in directory_usage_list:

        cmd = "find '{0}' -type f | sed 's/.*\.//' | sort | uniq -c".format(i[1])

        p = Popen(cmd, stdout=PIPE, stderr=PIPE, bufsize=256*1024*1024, shell=True)
        
        file_count, file_info = p.communicate()
        
        data.append(i[1] + "," + i[0] + "," + file_count.replace('\n',' ').replace('\t',''))
        
    return data 

report_data = gen_directory_report(sys.argv[1])

print "Directory Name, Directory Size, Directory File Type Count"

for i in report_data:
    i.replace('\n', ',')
    print i
