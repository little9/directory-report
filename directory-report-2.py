#!/usr/bin/env python

# This script generates a report that provides information about files on the archive server


import sys, csv, os, magic
from subprocess import Popen, PIPE
from math import log

unit_list = zip(['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'], [0, 0, 1, 2, 2, 2])

def sizeof_fmt(num):
    """Human friendly file size"""
    if num > 1:
        exponent = min(int(log(num, 1024)), len(unit_list) - 1)
        quotient = float(num) / 1024**exponent
        unit, num_decimals = unit_list[exponent]
        format_string = '{:.%sf} {}' % (num_decimals)
        return format_string.format(quotient, unit)
    if num == 0:
        return '0 bytes'
    if num == 1:
        return '1 byte'


def create_csv(csv_file, report_data):
    with open(csv_file, 'wb') as csvfile:
        field_names = ['name', 'file_type', 'mime_type', 'file_size', 'parent_directory', 'last_access', 'last_modified']
        writer = csv.DictWriter(csvfile, dialect=csv.excel, quotechar='"', quoting=csv.QUOTE_NONNUMERIC,fieldnames=field_names)
        writer.writeheader()
        for line in report_data:
            writer.writerow(line)

def gen_directory_report(path):

    filelist = []
    
    for dirpath, dirnamess, filenames in os.walk(path, topdown=False):

        for filename in filenames:
            complete_name = os.path.join(dirpath, filename)
           
            file_type = magic.from_file(complete_name)
            mime_type = magic.from_file(complete_name, mime=True)
            file_stat = os.stat(complete_name) 
            file_size = sizeof_fmt(file_stat.st_size)
            last_access = file_stat.st_atime
            last_modified = file_stat.st_mtime

            data = { 'name':complete_name, 'file_type':file_type, 'mime_type':mime_type, 'file_size':file_size , 'parent_directory': dirpath, 'last_access' : last_access, 'last_modified' : last_modified }
            filelist.append(data)


    return filelist
    



report_data = gen_directory_report(sys.argv[1])

print gen_directory_report(sys.argv[1])

create_csv("test.csv", report_data)

#print "Directory Name, Directory Size, Directory File Type Count"





