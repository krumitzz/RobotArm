import os
from re import sub
import subprocess
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

def mkVenvUbuntu(vpath):
    """
    Creates a python virtual environment on ubuntu
    """
    if os.path.isdir(vpath):
        print('virtual env exists, activate it instead')
        return False
    
    try:
        try:
            subprocess.Popen(['virtualenv', f'{vpath}'])
            os.mkdir('scripts')
            with open('scripts/env', mode='w', encoding='utf8') as file:
                text=f"#!/bin/bash\nsource {vpath}/bin/activate\nalias activate='source {vpath}/bin/activate'"
                file.write(text)
            subprocess.run(['chmod', 'u+x', 'scripts/env'])
            #subprocess.run(['{vpath}/bin/python', '-m', 'pip', 'install -r requirements.txt'])
        except FileExistsError:
            return True
    except Exception as e:
        print(e)
        return False

    return True

def installPostgres():
    """
    installs a postgresql database server
    """
    with open(f'{BASE_DIR}/logfile', mode='w', encoding='utf8') as file:
        subprocess.run(['./install_postgresql_server'], stdout=file, cwd=f'{BASE_DIR}/scripts')

def postgresCreate(db_name, db_user, db_host='localhost', db_port='5432'):
    """
    creates a postgresql database
    """
    installPostgres()
    print('creating postgresql database...')
    with open('{BASE_DIR}/logfile', mode='w', encoding='utf8') as file:
        subprocess.run([
            'createdb', 
            f'-h {db_host}', 
            f'-p {db_port}',
            f'-U {db_user}',
            f'{db_name}'], stderr=file)
