#!/usr/bin/python3
"""This module contains the entry point of the command interpreter"""
import cmd


class HBNBCommand(cmd.Cmd):
    """Entry point of the command interpreter"""
    prompt = "(hbnb) "

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """Quit the program"""
        return True

    def postloop(self):
        print()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
