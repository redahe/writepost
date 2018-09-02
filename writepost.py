#!/usr/bin/python

import tempfile
import datetime
import os
import sys
import argparse
import conf

TEMPLATE = 'template.org'
COMMAND = conf.run_editor

TITLE_SECTION='#+TITLE:'
TARGET_SECTION='#+TARGET:'
POSTED_SECTION='#+POSTED_TO:'

YES = ['yes', 'ye', 'y']
NO = ['no', 'n']

title=None

def yes_no_question(question, default_yes=True):
    if default_yes:
        suff=' (Y/n): '
    else:
        suff=' (y/N): '
    reply = str(raw_input(question+suff)).lower().strip()
    if len(reply) == 0:
        return default_yes
    if reply in YES:
        return True
    if reply in NO:
        return False
    return yes_no_question(question, default_yes=True)


def create_template():
    tmp = tempfile.NamedTemporaryFile(suffix='.org', delete=False)
    with open(TEMPLATE) as source:
            tmp.write(source.read())
    tmp.close()
    return tmp.name


def edit(path):
    os.system(COMMAND + ' ' + path)


def add_posted_mark(path, service):
    with open(path) as f:
        content = f.readlines()

    found = False
    for i in range(len(content)):
        line = content[i].strip()
        if line.startswith(POSTED_SECTION):
            found = True
            pstd=line.split()
            if service in pstd:
                return
            else:
                suff = ' '+service if not line.endswith(' ') else service
                content[i] = line+suff+os.linesep
    if not found:
        content.append(POSTED_SECTION + ' ' + service)
    with open(path, 'w') as f:
        f.writelines(content)


def handle(path):
    services = set()
    posted_to = set()
    with open(path) as f:
        for line in f:
            if line.startswith(TITLE_SECTION):
                global title
                title=line[len(TITLE_SECTION):]
            if line.startswith(TARGET_SECTION):
                for s in line[len(TARGET_SECTION):].split():
                    services.add(s)
            if line.startswith(POSTED_SECTION):
                for s in line[len(POSTED_SECTION):].split():
                    posted_to.add(s)
    if not(services):
        print('No targets were specified.')
        return
    if not(services-posted_to):
        print('This message was already posted to all targets earlier. Exiting')
        return
    for service in services-posted_to:
        to_post = yes_no_question('Post to '+service+'?')
        if to_post:
            try:
                serv_module = __import__("post_"+service)
                if serv_module.post(path):
                    add_posted_mark(path, service)
                else:
                    print('was not posted to '+service)
                    change = yes_no_question('Change the post?')
                    if change:
                        edit(path)
                        handle(path)
                    return
            except ImportError as e:
                print('Error: module post_'+service+'.py not found')
                change = yes_no_question('Change the post?')
                if change:
                    edit(path)
                    handle(path)
                return


def save_post(path):
    global title
    folder=conf.save_folder
    folder = os.path.expanduser(os.path.expandvars(folder))
    if not os.path.exists(folder):
        os.system('mkdir -p '+folder)
    name=title.replace(' ', '_').strip()+datetime.datetime.now().strftime("%d._%B_%Y_%I_%M%p")
    dest = folder+os.path.sep+name
    os.system('cp '+ path + ' ' + dest)
    print 'Saved to: ' + dest


def main():
    parser = argparse.ArgumentParser(description='Post a message to blogs.')
    parser.add_argument('file', nargs='?', default=None, help='file to open')
    args =  parser.parse_args()
    if args.file:
        edit(args.file)
        handle(args.file)
    else:
        path = create_template()
        time1 = os.stat(path).st_mtime
        edit(path)
        time2 = os.stat(path).st_mtime
        if time1 != time2:
            handle(path)
            if yes_no_question('Save post?'):
                save_post(path)
        else:
            print 'Canceled'
        os.remove(path)



if __name__ == '__main__':
    main()
