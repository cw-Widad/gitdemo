#!/usr/bin/python

import os, stat, datetime
import sys
import argparse
from pathlib import Path

def main(args):


    namespace, _ = parser.parse_known_args(args)  # namespace include flag value pairs while extra is the first argument, python filename
    args_dict = vars(namespace)

    # print(args_dict)

    # args = parser.parse_args(args)
    root_dir = args_dict['ls']

    # print folder names for multi-subfolders
    for dir in root_dir:  

        # initialize for longformat
        longformat_dict = {'block_sizes':[], 'permissions':[], 'linkcounts':[], 'owners':[], 
                           'groups':[], 'filesizes':[], 'months':[], 'dates':[], 'times':[], 'filenames':[]}
        if len(root_dir) > 1:
            print(dir + ':')
     
        dir_ls = os.listdir(dir) # get (complete) directory list  

        ## if use -a mode, add current and parent folders
        if args_dict['a']:
            dir_ls.append('.')
            dir_ls.append('..')
        else:
            dir_ls = [x for x in dir_ls if not x[0]=='.']

        num_file = len(dir_ls) # real files numbers

        ## for -l : longformat
        if args_dict['l']:
            for filename in sorted(dir_ls):
                file_dir = os.path.abspath(os.path.join(dir, filename))

                # toooo debug
                # file_dir = '/home/chenxue/cloudwuerdig_practice/python/.venv/bin/Activate.ps1'

                # add file mode
                file_mode = stat.filemode(os.lstat(file_dir).st_mode)
                longformat_dict['permissions'].append(file_mode)
                # add block size
                if file_mode[0] == 'l':
                    block_size = 0
                else:
                    block_size = -(-os.lstat(file_dir).st_size //4096) * 4 # current directory + filename -> absolute file path -> get file size -> save 
                longformat_dict['block_sizes'].append(block_size)
                # add link count
                link_count = os.stat(file_dir).st_nlink
                longformat_dict['linkcounts'].append(link_count)
                # add owner and group
                longformat_dict['owners'].append(Path(file_dir).owner())
                longformat_dict['groups'].append(Path(file_dir).group())
                # add file size
                file_size = -(-os.lstat(file_dir).st_size )
                longformat_dict['filesizes'].append(file_size)
                # add lastaccess
                last_access = datetime.datetime.fromtimestamp(os.stat(file_dir).st_atime)
                month, date, time = last_access.strftime("%B, %d, %I:%M").split(',')
                longformat_dict['months'].append(month)
                longformat_dict['dates'].append(date)
                longformat_dict['times'].append(time)
                # add file
                longformat_dict['filenames'].append(filename)

            ## start to print
            total = sum(longformat_dict['block_sizes'])
            print(f'total {total}')
            

            ## print results that depends on -s mode, print block at first column if -s is the case
            if args_dict['s'] :  # modified for -s mode
                for i in range(num_file):
                    filename = longformat_dict['filenames'][i]
                    if ' ' in filename:
                        filename = f'\'{filename}\''
                    
                    print(f"{str(longformat_dict['block_sizes'][i]):>2}  {str(longformat_dict['permissions'][i]):} {str(longformat_dict['linkcounts'][i]):} {str(longformat_dict['owners'][i]):>10}{str(longformat_dict['groups'][i]):>10}{str(longformat_dict['filesizes'][i]):>5}{str(longformat_dict['months'][i]):>5}{str(longformat_dict['dates'][i]):>5}{str(longformat_dict['times'][i]):<5} {filename:<3}")
            else: # for mode without -s
                for i in range(num_file):  
                    filename = longformat_dict['filenames'][i]
                    if ' ' in filename:
                        filename = f'\'{filename}\''
                    
                    print(f"{str(longformat_dict['permissions'][i]):} {str(longformat_dict['linkcounts'][i]):} {str(longformat_dict['owners'][i]):>10}{str(longformat_dict['groups'][i]):>10}{str(longformat_dict['filesizes'][i]):>5}{str(longformat_dict['months'][i]):>5}{str(longformat_dict['dates'][i]):>5}{str(longformat_dict['times'][i]):<5} {filename:<3}")

            print('\n')

        else:
                for filename in sorted(dir_ls):
                    if ' ' in filename:
                        sys.stdout.write(f'\'{filename}\' ')
                    else:
                        sys.stdout.write(filename + ' ')
                print('\n')
                

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usage: ls [OPTION]... [FILE]... \n List information about the FILEs (the current directory by default). \n Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.")
    parser.add_argument("ls", help="List information about the FILEs (the current directory by default).", type=str, default=".", nargs='*')
    parser.add_argument("-l", help="use a long listing format", action="store_true")
    parser.add_argument("-a", help="do not ignore entries starting with .", action="store_true")
    parser.add_argument("-s", help="print the allocated size of each file, in blocks", action="store_true")

    # sys.argv = ['task2.py', '-al', '..', './testfolder2', './.venv/bin/']        # Uncomment this line to debug

    ## run the script in shell: python3 List_lsa.py -lsa <folder1> <folder2> <folder3>
    
    main(sys.argv[1:])