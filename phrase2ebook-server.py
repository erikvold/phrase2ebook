# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 18:44:35 2016

@author: fred
"""
import subprocess
import os
import psutil
import json
import shlex
from flask import Flask, request, send_from_directory

import configparser
config = configparser.ConfigParser()
config.read("config.ini")
commandpath = config.get("Paths", "commandpath")
mycwd = config.get("Paths", "mycwd")
print('local commandpath and working directory are ' + commandpath, mycwd)


from two1.wallet import Wallet
from two1.bitserv.flask import Payment

# Configure the app and wallet
app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

@app.route('/buy', methods=['GET', 'POST'])
@payment.required(10000)


def buy_bookbuild():

    flags = json.loads(request.data.decode('UTF-8'))
    print('options received are ' + flags['options'])
    optvalue = str(flags['options'])
    optvalue = commandpath + ' ' + optvalue
    print('command line will be ' + optvalue)
    args = shlex.split(optvalue)
    print(args)
    status = subprocess.check_output(args, cwd = mycwd)
    return status, send_from_directory('/tmp/pagekicker/', '4stdout.txt')


# Initialize and run the server
if __name__ == '__main__':

   import click

   @click.command()
   @click.option("-d", "--daemon", default=False, is_flag=True,
                  help="Run in daemon mode.")

   def run(daemon):
            if daemon:
                pid_file = './phrase2-ebooks.pid'
                if os.path.isfile(pid_file):
                    pid = int(open(pid_file).read())
                    os.remove(pid_file)
                    try:
                        p = psutil.Process(pid)
                        p.terminate()
                    except:
                        pass
                try:
                    p = subprocess.Popen(['python3', 'phrase2ebook-server.py'])
                    open(pid_file, 'w').write(str(p.pid))
                except subprocess.CalledProcessError:
                    raise ValueError("error starting phrase2-ebook.py daemon")
            else:
                print("phrase2-ebook running...")
                app.run(host='::', port=5034, debug=True)
   run()
