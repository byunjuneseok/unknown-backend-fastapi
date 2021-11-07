#!/usr/bin/env python3
import subprocess

import env


if __name__ == '__main__':

    cmd_common = ['mysql']
    cmd_common += ['-h' + env.db_host]
    cmd_common += ['-P' + env.db_port]
    cmd_common += ['-u' + env.db_user]
    cmd_common += ['-p' + env.db_password]
    cmd_common += ['-f']

    with open('mysql_dump.sql', 'r') as f:
        p = subprocess.Popen(cmd_common, stdin=f)
        p.communicate()
        if p.returncode != 0:
            raise Exception()
        f.close()
