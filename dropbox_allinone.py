#!/usr/bin/env python
from __future__ import print_function
import argparse
import os
import sys

try:
    import dropbox
    from dropbox.client import DropboxClient
except:
    print('Dropbox module is not installed. Please install it with command: \nsudo pip install dropbox')

#auth_token = 'SU7cL62oa6AAAAAAAAAAC4ENTNuBqA3K8wH9ZdKpseYBrPdUO6hc92rMW9gphzCn'

parser = argparse.ArgumentParser(description='Command line tool for Dropbox')
parser.add_argument('-l', '--list', help='List files in a folder')
parser.add_argument('-d', '--download', help='Download folder from remote server')
parser.add_argument('-u', '--upload', nargs='+', help='Upload folder to remote server')
parser.add_argument('-t', '--token', nargs='+', help='Please enter token', required=True)

args = parser.parse_args()
folder = args.list
auth_token = args.token[0]
src = args.upload[0]
dst = args.upload[1]
to_download = args.download

try:
    dbx = dropbox.Dropbox(auth_token)
    client = DropboxClient(auth_token)
    folder_metadata = client.metadata('/')
except:
    print('Invalid Token. Please check your token and try again...')
    sys.exit(1)


def get_files(folder):
    l = []
    res = dbx.files_list_folder(folder)
    for entry in res.entries:
        l.append(entry.path_display)
    return l


def upload():
#    src = args.upload[0]
#    dst = args.upload[1]
    if os.path.exists(src):
        if os.path.isfile(src):
            path = os.path.abspath(src)
            with open(path, 'rb') as f:
                client.put_file('/' + dst + '/' + src, f)
                print('Uploaded: ' + src + ' ')
                sys.exit(1)
        else:
            files = os.listdir(src)
            for each in files:
                path = os.path.abspath(src+'/'+each)
                if os.path.isfile(path):
                    with open(path, 'rb') as f:
                        client.put_file('/' + dst + '/' + each, f)
                        print('Uploaded: ' + each + ' ')
                else:
                    subfolder(path)
                   # subdir = os.listdir(path)
                   # for a in subdir:
                   #     path = os.path.abspath(src+'/'+each+'/'+a)
                   #     print(path)
                   #     with open(path, 'rb') as f:
                   #         client.put_file('/' + dst + '/' + each, f)
                   #         print('Uploaded: ' + a + ' ')
    else:
        print('Source directory does not exists. Please enter proper directory')
        sys.exit(1)

def subfolder(folder):
    files = os.listdir(folder)
    for each in files:
      path = os.path.abspath(folder+'/'+each)
      #print(path)
      if os.path.isfile(path):
        d = path.replace(src,'')
        final = '/'+dst+'/'+d
        with open(path, 'rb') as f:
          client.put_file(final, f)
          print('Uploaded: ' + each + ' ')
      else:
        subfolder(path)

def download():
    print(to_download)
    try:
        dbx.files_list_folder('/'+to_download)
        print('Downloading folder')
        l = get_files('/'+to_download)
        print(l)
        for each in l:
            print('Downloding ' + each)
            md, res = dbx.files_download(each)
            data = res.content
            to_write = each.split('/')[-1]
            with open(to_write, 'w') as f:
                f.write(data)
    except:
        print('Looks like you want to download just one file')
        md, res = dbx.files_download(to_download)
        data = res.content
        to_write = to_download.split('/')[-1]
        with open(to_write, 'w') as f:
            f.write(data)

if args.list:
    l = get_files('/'+folder)
    for each in l:
        print(each)

if args.upload:
    upload()

if args.download:
    download()
