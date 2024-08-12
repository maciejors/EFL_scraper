import re

import pandas as pd

from . import commands


available_commands = {
    'help': commands.print_help,
    'list': commands.list_fixtures,
    'competition': commands.competition_cmd,
    'club': commands.club_cmd,
}


def _parse_command(user_input: str, df_fixtures: pd.DataFrame) -> None:
    tokens = re.split('\\s+', user_input, maxsplit=1)
    command_name = tokens[0]

    if command_name not in available_commands.keys():
        print(f'{command_name} is an unknown command. '
              'Type "help" to view the list of available commands')
        return

    command_caller = available_commands[command_name]
    if len(tokens) == 1:
        command_caller(df_fixtures)
    else:
        argument = tokens[1]
        command_caller(df_fixtures, argument)


def run_shell(df_fixtures: pd.DataFrame) -> None:
    print('Welcome to the data browser! To exit, type "exit" or "quit".', end='\n\n')
    commands.print_help(df_fixtures)

    inp = input('> ').strip()
    while inp not in {'exit', 'quit'}:
        if len(inp) == 0:
            continue
        _parse_command(inp.strip(), df_fixtures)
        inp = input('> ').strip()
