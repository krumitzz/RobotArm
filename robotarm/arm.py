#!/usr/bin/python3
"""
RobotArm entry script v0.02
"""
import controllers
import os
import pathlib
import sys

#BASE_DIR = pathlib.Path(__file__).resolve().parent

# maps keys to controller method
STATE_CONTROLLERS = {
    'list': 'controllers.StateController().list',
    'create': 'controllers.StateController().create',
    'activate': 'controllers.StateController().activate',
    'stop': 'controllers.StateController().stop',
    'delete': 'controllers.StateController().delete',
}

COMMAND_CONTROLLERS = {
    'execute': 'controllers.CommandController().executeCommand',
    'list': 'controllers.CommandController().listCommands'
}

TEST_CONTROLLERS = {
    'run': 'cotrollers.TestController().run'
}

API_SERVICE_CONTROLLERS = {
    'status': 'controllers.APIServiceController().health_check',
    'start': 'controllers.APIServiceController().start_service',
    'stop': 'controllers.APIServiceController().stop_service'
}

def main():
    # maps keys to controller classes
    options = {
        ('-v', '--version'): 'v0.01',
        ('-h', '--help'): 'help',
        ('-s', '--state'): STATE_CONTROLLERS,
        ('-c', '--command'): COMMAND_CONTROLLERS,
        ('-t', '--test'): TEST_CONTROLLERS,
        ('-p', '--pipline'): 'Pipeline controller/handler',
        'service': API_SERVICE_CONTROLLERS,
    }

    # extract file name and remove it
    args = sys.argv
    args_length = len(args)  # store args length

    arm_usage = 'Usage'
    file_name = args[0]

    # make sure length isn't less than 2
    if args_length < 2:
        exit(arm_usage)

    # remove file name
    del(args[0])

    # extract option and check if
    # option is valid
    option = args[0]

    # remove option
    del(args[0])

    # check if option is version or help
    if args_length == 2:
        # Prints arm script version or help
        if option in ('-v', '-h', '--version', '--help'):
            for option_keywords in options.keys():
                if option in option_keywords:
                    print(options[option_keywords])
            exit()
        else:
            exit(arm_usage)

    # builds controller path
    # fails if controller method doesn't exists
    try:
        for keyword_options in options.keys():
            if option in keyword_options or option is keyword_options:
                keyword_option = options[keyword_options]
        try:
            if keyword_option is COMMAND_CONTROLLERS:
                try:
                    eval(keyword_option[args[0]])(args)
                except KeyError:
                    eval(keyword_option['execute'])(args)
                exit()
            if keyword_option is API_SERVICE_CONTROLLERS:
                eval(keyword_option[args[0]])()
            else:
                # passes all arguments into controller method for now
                eval(keyword_option[args[0]])(args)
        except UnboundLocalError:
            exit('Uknown keyword option')
    except KeyError:
        exit('Unknown keyword option action')

if __name__ == '__main__':
    main()