#!/usr/bin/python3
"""
Contains Handler for handling states related funtions
"""
from flask import current_app
from robotarm.states.django_state import DjangoState
from robotarm.handlers import helpers
import os
from robotarm import states
import subprocess
import yaml

# TODO: make a database handler
# TODO: implement git init repo method
# TODO: improve provision environment, make it more interactive


class StateHandler:
    """
    handles state related funtions, utilized by state apis

    methods:
        getCurrentSate
        activate
        deactivate
        createState
        deleteState
        all_states
        provisionEnv
    """
    SUPPORTED_FRAMEWORKS = {
        'django': 'states.django_state.DjangoState'
    }

    SUPPORTED_DATABASE = {
        'postgresql': 'helpers.postgresCreate'
    }

    def getCurrentState(self):
        """
        Returns the current state
        """
        id = states.storage.all()['current_state']['id']
        if id != None:
            return states.storage.get(id)
        return None

    def activate(self, id):
        """
        activates a state by setting it as current state

         Args:
            id [uuid]: unique identifier of states object

        Returns:
            None if setCurrentState returns None
        """
        state = states.storage.setCurrentState(id)
        states.storage.save()

        wd = state.working_dir
        if os.path.isdir(wd) and os.getcwd() != wd:
            os.chdir(wd)

        vpath = state.virtual_venvs[0]
        try:
            os.mkdir('scripts')
            with open('scripts/env', mode='w', encoding='utf8') as file:
                text = f"#!/bin/bash\nsource {vpath}/bin/activate\nalias activate='source {vpath}/bin/activate'"
                file.write(text)
            subprocess.Popen(['chmod', 'u+x', 'scripts/env'])
        except FileExistsError:
            pass
        return state

    def deactivate(self):
        """
        deactivates the current state
        """
        states.storage.removeCurrentState()

    def createState(self, **kwargs):
        """
        Parses a Yaml File into a python native dictionary objects
        and creats a state

         Args:
            file_name [string]: name of or path to file

        Returns:

        """
        file_name = kwargs['file']
        yaml_dict = self.parseYamlFile(file_name)

        if yaml_dict:
            framework = yaml_dict['framework']

            if framework in self.SUPPORTED_FRAMEWORKS.keys():
                state = eval(self.SUPPORTED_FRAMEWORKS[framework])(**yaml_dict)
                state.save()
                print('---state saved---')

                # print('activating state...')
                # state = self.activate(state.id)
                #print(f'{state.project_name} activated')

                print('setting up environment, this may take a few minutes...')
                self.provisionEnv(state)
                print('done.')
                return state
            else:
                exit('Unsurppoted framework')

    def deleteState(self, id):
        """
        deletes a state object

         Args:
            id [uuid]: unique identifier of states object

        Returns:
            None if state does not exists
        """
        try:
            states.storage.delete(id)
        except Exception:
            return None

    @staticmethod
    def parseYamlFile(file):
        """
        tries to open and parse a yaml file to dictionary object
        """
        pwd = os.getcwd()
        os.chdir(pwd)
        try:
            with open(f'{file}', mode='r', encoding='utf8') as file:
                yaml_dict = yaml.full_load(file)
                return yaml_dict
        except FileNotFoundError:
            print("file not found")

    @staticmethod
    def all_states():
        """
        retrieves all states objects
        """
        states_objs = states.storage.all()
        state_dict = {}

        for key, value in states_objs.items():
            if key != 'current_state':
                state_dict[key] = {'name': value.project_name, 'version': value.version}
        state_dict['current_state'] = states_objs['current_state']
        
        return state_dict

    def provisionEnv(self, state):
        """
        provision a development environment based on state object

        Args:
            state [__class__]: a __class__.BaseState object
        """
        wd = state.working_dir
        if os.path.isdir(wd) and os.getcwd() != wd:
            os.chdir(wd)

        if state.virtual_venvs:
            venvs = state.virtual_venvs
            vpath = venvs[0]
            created = helpers.mkVenvLinux(vpath)

            if created:
                print(f'created virtual environment at {vpath}')

        # if state.database:
        #     database = state.database[0]
        #     try:
        #         print(database)
        #         eval(self.SUPPORTED_DATABASE[database['type']])(database['name'], database['user'])
        #     except Exception as e:
        #         raise(e)
