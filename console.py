#!/usr/bin/python3
"""This module contains the entry point of the command interpreter"""
import cmd
import re
from models import storage
from models.base_model import BaseModel


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
        print()
        return True

    def do_create(self, line):
        """Creates a new instance of BaseModel"""
        if not line:
            print("** class name missing **")
        elif not storage.actual_class(line):
            print("** class doesn't exist **")
        else:
            obj = storage.actual_class(line)()
            obj.save()
            print(obj.id)

    def do_show(self, line):
        """Prints the string representation of an instance"""
        if not line:
            print("** class name missing **")
        else:
            args = line.split(' ')
            if not storage.actual_class(args[0]):
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                obj_id = "{}.{}".format(args[0], args[1])
                if obj_id not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[obj_id])

    def do_destroy(self, line):
        """Deletes an instance"""
        if not line:
            print("** class name missing **")
        else:
            args = line.split(' ')
            if not storage.actual_class(args[0]):
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                obj_id = "{}.{}".format(args[0], args[1])
                if obj_id not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[obj_id]
                    storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances"""
        if line:
            args = line.split(' ')
            if not storage.actual_class(args[0]):
                print("** class doesn't exist **")
            else:
                all_list = [
                        str(obj) for key, obj in storage.all().items()
                        if type(obj).__name__ == args[0]]
                print(all_list)
        else:
            all_list = [str(obj) for key, obj in storage.all().items()]
            print(all_list)

    def do_update(self, line):
        """Updates an instance by adding or updating an attribute"""
        if not line:
            print("** class name missing **")
            return
        exp = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(exp, line)
        cln = match.group(1)
        u_uid = match.group(2)
        attr = match.group(3)
        val = match.group(4)
        if not match:
            print("** class name missing **")
        elif not storage.actual_class(cln):
            print("** class doesn't exist **")
        elif u_uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(cln, u_uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attr:
                print("** attribute name missing **")
            elif not val:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', val):
                    if '.' in val:
                        cast = float
                    else:
                        cast = int
                else:
                    val = val.replace('"', '')
                attribs = storage.attrs(cln)
                if attribs and attr in attribs:
                    val = attribs[attr](val)
                elif cast:
                    try:
                        val = cast(val)
                    except ValueError:
                        pass
                setattr(storage.all()[key], attr, val)
                storage.all()[key].save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
