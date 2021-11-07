#!/usr/bin/env python3
import re
import subprocess
from subprocess import PIPE

import env


def _manual_backup():
    host = env.db_host
    db_name = env.db_name
    password = env.db_password
    user = env.db_user

    _mysql_dump(host, user, password, db_name, './mysql_schema.sql')


def _mysql_dump(host, user, password, database, filename_path):

    cmd = ['mysqldump']
    cmd += ['-h' + host]
    cmd += ['-u' + user]
    cmd += ['-p' + password]
    cmd += ['--column-statistics=0']
    cmd += ['--comments']
    cmd += ['--databases', database]
    cmd += ['--no-data']
    cmd += ['--set-gtid-purged=OFF']

    print('\n>>> ' + ' '.join(cmd) + '\n')

    filename_path_raw = filename_path + '.raw'

    with open(filename_path_raw, 'w') as ff:
        subprocess.Popen(cmd, stdout=ff).communicate()

    with open(filename_path_raw, 'r') as ff_raw, open(filename_path, 'w') as ff:
        while True:
            line = ff_raw.readline()
            if not line:
                break

            if line.startswith('-- MySQL dump') or \
                    line.startswith('-- Host') or \
                    line.startswith('-- Server version') or \
                    line.startswith('-- Dump completed on'):
                ff.write('\n')
                continue

            line = re.sub(' AUTO_INCREMENT=[0-9]*', '', line)
            ff.write(line)

    cmd = ['rm', filename_path_raw]

    subprocess.Popen(cmd, stdout=PIPE).communicate()

if __name__ == '__main__':
    _manual_backup()
