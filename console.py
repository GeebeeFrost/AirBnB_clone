#!/usr/bin/python3
"""This module contains the entry point of the command interpreter"""
import cmd
import re
from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """Entry point of the command interpreter"""
    prompt = "(hbnb) "

    def default(self, line):
        """Catch non-matching commands."""
        self.parse_cmd(line)

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
        """Creates a new instance of a specified class"""
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
        """Deletes an instance based on class name and id"""
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
    
    def do_count(self, line):
        """Counts the instances of a class.
        """
        args = line.split(' ')
        if not args[0]:
            print("** class name missing **")
        elif not storage.actual_class(args[0]):
            print("** class doesn't exist **")
        else:
            matches = [
                k for k in storage.all() if k.startswith(
                    args[0] + '.')]
            print(len(matches))

    def parse_cmd(self, line):
        """Intercepts commands to test for class.syntax()"""
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line
        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(
                    1) or "") + " " + (match_attr_and_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(command)
        return command


if __name__ == "__main__":
    HBNBCommand().cmdloop()
