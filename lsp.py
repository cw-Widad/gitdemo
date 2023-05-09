#!/usr/bin/pythoin

#on to some coding

import os
import argparse
import stat
def longformat(filepath):
    path = os.path.abspath(filepath)
    filelist = os.listdir(filepath)
    #[print(os.path.join(path,i)) for i in filelist]
    for i in filelist:
        abspath = os.path.join(path,i)
        stats = os.stat(abspath)
        if not i.startswith('.'):
           print(f"{stat.filemode(stats.st_mode)} {stats.st_nlink}      {stats.st_uid}       {stats.st_gid}       {stats.st_size}        {stats.st_atime}      {i}")


#comment

#even more value right here.

#more useful comments
#start afresh
# check commit sign - Widad3
