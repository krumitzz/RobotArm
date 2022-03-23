"""
Command Handler module
"""
from calendar import c
from flask import current_app
import states
from handlers import StateHandler


class CommandHandler:
    """
    communicates with api and returns required state
    information on how to handle commands 
    """

    @staticmethod
    def getEntryCommand():
        """
        gets current activated state and returns it's management
        entry command if available and the current working directory
        """
        current_state = StateHandler().getCurrentState()

        response_dict = {
            'working_dir': current_state.working_dir,
            'entry_command': current_state.entry_command   
        }
        return response_dict

    @staticmethod
    def getAllCommands():
        pass
