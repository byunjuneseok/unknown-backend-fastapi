#!/usr/bin/env python3
import subprocess
from datetime import datetime

import env

cmd_common = ['mysql']
cmd_common += ['-h' + env.db_host]
cmd_common += ['-P' + env.db_port]
cmd_common += ['-u' + env.db_user]
cmd_common += ['-p' + env.db_password]


if __name__ == '__main__':
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(' '.join(['Started at:', start_time]))

    cmd = cmd_common + ['-e', f'DROP DATABASE IF EXISTS `{env.db_name}`;']
    print(cmd)
    subprocess.Popen(cmd).communicate()

    cmd = cmd_common + ['-e', f'CREATE DATABASE `{env.db_name}` CHARACTER SET utf8;']
    subprocess.Popen(cmd).communicate()

    cmd = cmd_common + ['--comments']

    filename = './mysql_schema.sql'
    with open(filename, 'r') as f:
        subprocess.Popen(cmd, stdin=f).communicate()
