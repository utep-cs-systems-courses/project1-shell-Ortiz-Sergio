#! /usr/bin/env python3

import os, sys, time, re

def mario_intro():
    
    print("____▒▒▒▒▒")
    print("—-▒▒▒▒▒▒▒▒▒")
    print("—–▓▓▓░░▓░")
    print("—▓░▓░░░▓░░░")
    print("—▓░▓▓░░░▓░░░")
    print("—▓▓░░░░▓▓▓▓")
    print("——░░░░░░░░")
    print("—-▓▓▒▓▓▓▒▓▓")
    print("–▓▓▓▒▓▓▓▒▓▓▓")
    print("▓▓▓▓▒▒▒▒▒▓▓▓▓")
    print("░░▓▒░▒▒▒░▒▓░░")
    print("░░░▒▒▒▒▒▒▒░░░")
    print("░░▒▒▒▒▒▒▒▒▒░░")
    print("—-▒▒▒ ——▒▒▒")
    print("–▓▓▓———-▓▓▓")
    print("▓▓▓▓———-▓▓▓▓")
    print(" ")

def shell(arg1, arg2):
    output_redirect = False
    output_file = "";
    
    print("Would you like to redirect output?")
    if input("yes /no ").lower() == "yes":
        output_redirect = True
        output_file = input("What file would you like to redirect to? ")

    pid = os.getpid()

    os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
    
    rc = os.fork()
    
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
        
    elif rc == 0:
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %  (os.getpid(), pid)).encode())
        args = [arg1, arg2]

        if output_redirect:
            os.close(1)
            os.open(output_file, os.O_CREAT | os.O_WRONLY);
            os.set_inheritable(1, True)
        
        for dir in re.split(":", os.environ['PATH']):
            
            program = "%s/%s" % (dir, args[0])
            os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
            try:
                os.execve(program, args, os.environ)
                
            except FileNotFoundError: 
                pass 

        os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
        sys.exit(1)

    else:
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %  (pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" %  childPidCode).encode())

def main():
    mario_intro()
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
