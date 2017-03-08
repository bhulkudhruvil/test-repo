#!/usr/bin/env python
from __future__ import print_function
import dropbox
import argparse
import os
import sys
from dropbox.client import DropboxClient
#auth_token = 'SU7cL62oa6AAAAAAAAAAC4ENTNuBqA3K8wH9ZdKpseYBrPdUO6hc92rMW9gphzCn'

parser = argparse.ArgumentParser(description='Command line tool for Dropbox')
parser.add_argument('-l','--list',help='List files in a folder')
parser.add_argument('-d','--download',help='Download folder from remote server')
parser.add_argument('-u','--upload',nargs='+',help='Upload folder to remote server')
parser.add_argument('-t','--token',nargs='+',help='Please enter token',required=True)

args=parser.parse_args()
folder = args.list
auth_token = args.token[0]
to_download = args.download

dbx=dropbox.Dropbox(auth_token)
client=DropboxClient(auth_token)

def get_files(folder):
  l=[]
  res = dbx.files_list_folder(folder)
  for entry in res.entries:
    l.append(entry.path_display)
  return l

def upload():
  src = args.upload[0]
  dst = args.upload[1]
  if os.path.exists(src):
    if os.path.isfile(src):
      path=os.path.abspath(src)
      with open(path,'rb') as f:
        client.put_file('/'+dst+'/'+src,f)
        print('Uploaded: '+src +' ')
        sys.exit(1)
    else:
      files = os.listdir(src)
      for each in files:
        path=os.path.abspath(src+'/'+each)
        with open(path,'rb') as f:
          client.put_file('/'+dst+'/'+each,f)
          print('Uploaded: '+each +' ')
  else:
    print('Source directory does not exists. Please enter proper directory')
    sys.exit(1)

def download():
  print(to_download)
  try:
    dbx.files_list_folder('/'+to_download)
    print('Downloading folder')
    l=get_files('/'+to_download)
    print(l)
    for each in l:
      print('Downloding '+each)
      md,res = dbx.files_download(each)
      data = res.content
      to_write = each.split('/')[-1]
      with open(to_write,'w') as f:
        f.write(data)
  except:
    print('Looks like you want to download just one file')
    md,res = dbx.files_download(to_download)
    data = res.content
    to_write = to_download.split('/')[-1]
    with open(to_write,'w') as f:
      f.write(data)

if args.list:
  l=get_files('/'+folder)
  for each in l:
    print(each)

if args.upload:
  upload()

if args.download:
  download()
