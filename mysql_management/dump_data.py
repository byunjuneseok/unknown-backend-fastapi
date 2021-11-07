#!/usr/bin/env python3
import subprocess

import env

if __name__ == '__main_-':
    cmd = ['mysqldump']
    cmd += ['--column-statistics=0']
    cmd += ['--comments']
    cmd += ['--databases', env.db_host]
    cmd += ['--hex-blob']
    cmd += ['--no-create-info']
    cmd += ['--set-gtid-purged=OFF']
    cmd += ['--single-transaction']
    cmd += ['--skip-extended-insert']
    # cmd += ['--where=1 ORDER BY id DESC LIMIT 4000']
    cmd += ['-h' + env.db_host]
    cmd += ['-p' + env.db_password]
    cmd += ['-u' + env.db_user]

    print('\n>>> ' + ' '.join(cmd) + '\n')

    with open('./mysql_data.sql', 'w') as ff:
        p = subprocess.Popen(cmd, stdout=ff)
        p.communicate()
        if p.returncode != 0:
            raise Exception()
