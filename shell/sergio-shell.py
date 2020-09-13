#! /usr/bin/env python3

import os, sys, time, re

def shell(arg1, arg2):

    pid = os.getpid()

    os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
    
    rc = os.fork()
    
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
        
    elif rc == 0:                   # child
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
                     (os.getpid(), pid)).encode())
        args = [arg1, arg2]
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
            try:
                os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly

        os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
        sys.exit(1)                 # terminate with error

    else:                           # parent (forked ok)
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                     (pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                     childPidCode).encode())


def main():
    print("Welcome to Sergio Shell! Enter your command or 'exit' to terminate")
    user_command = input("$ ")

    while (user_command.lower() != "exit"):
        user_args = user_command.split()
        if len(user_args) < 2:
            print("Please enter at least two arguments")
            user_command = input("$ ")
            continue
        
        shell(user_args[0], user_args[1])
        user_command = input("$ ")

    print("Thank you for using my shell!")

if __name__ == "__main__":
    main()
