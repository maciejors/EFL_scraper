import cmd

import pandas as pd

from . import commands


class _BrowserShell(cmd.Cmd):
    intro = ('Welcome to the data browser! '
             'Type help or ? to list commands. '
             'Type exit or quit to close the shell.')
    prompt = 'efl_browser> '
    file = None

    def __init__(self, df_fixtures: pd.DataFrame):
        super().__init__()
        self.df_fixtures = df_fixtures

    def emptyline(self):
        return False

    def do_exit(self, arg):
        """Closes the shell"""
        return True

    def do_quit(self, arg):
        """Closes the shell"""
        return self.do_exit(arg)

    def do_list(self, arg):
        """List all fixtures"""
        commands.list_fixtures(self.df_fixtures)

    def do_competition(self, arg):
        """
        Lists all the fixtures for the specified competition.
        If competition is not specified, lists all available
        competitions instead
        """
        competition = arg if arg != '' else None
        commands.competition_cmd(self.df_fixtures, competition)

    def do_club(self, arg):
        """
        Lists all the fixtures for the specified club.
        If club is not specified, lists all available
        clubs instead
        """
        club = arg if arg != '' else None
        commands.club_cmd(self.df_fixtures, club)


def run_shell(df_fixtures: pd.DataFrame) -> None:
    _BrowserShell(df_fixtures).cmdloop()
