#! /usr/bin/env python3

import os, sys, time, re

def get_user_command():
    if os.environ.get("$PS1") != None:
        return input(os.environ["$PS1"])
    return input("$ ")

def intro():
    print("Art by Christian 'CeeJay' Jensen")
    print("                         .-.                   ")
    print("                        ( (                    ")
    print("                         `-'                   ")
    print("                                               ")
    print("                    .   ,- To the Moon Sergio !")
    print("                   .'.                         ")
    print("                   |o|                         ")
    print("                  .'o'.                        ")
    print("                  |.-.|                        ")
    print("                  '   '                        ")
    print("                   ( )                         ")
    print("                    )                          ")
    print("                   ( )                         ")
    print("                                               ")
    print("               ____                            ")
    print("          .-'""p 8o""`-.                       ")
    print("       .-'8888P'Y.`Y[ ' `-.                    ")
    print("     ,']88888b.J8oo_      '`.                  ")
    print("   ,' ,88888888888[\"        Y`.                ")
    print("  /   8888888888P            Y8\               ")
    print(" /    Y8888888P'             ]88\              ")
    print(":     `Y88'   P              `888:             ")
    print(":       Y8.oP '- >            Y88:             ")
    print("|          `Yb  __             `'|             ")
    print(":            `'d8888bo.          :             ")
    print(":             d88888888ooo.      ;             ")
    print(" \            Y88888888888P     /              ")
    print("  \            `Y88888888P     /               ")
    print("   `.            d88888P'    ,'                ")
    print("     `.          888PP'    ,'                  ")
    print("       `-.      d8P'    ,-'   -CJ-             ")
    print("          `-.,,_'__,,.-'                       ")
    print("                                               ")

def shell(args):
    output_redirect = False
    output_file = ""

    input_redirect = False
    input_file = ""

    if args.count(">") > 0:
        output_redirect = True
        output_file = args[args.index(">") + 1]

    if args.count("<") > 0:
        print("input redirect")
        input_redirect = True
        input_file = args[args.index("<") - 1]

    pid = os.getpid()
    
    rc = os.fork()
    
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
        
    elif rc == 0:

        if output_redirect:
            os.close(1)
            os.open(output_file, os.O_CREAT | os.O_WRONLY);
            os.set_inheritable(1, True)

        if input_redirect:
            os.close(0)
            fdIn = os.open(input_file, os.O_RDONLY);
            os.set_inheritable(0, True)

            args.remove(input_file)
            args.remove("<")

            list_counter = 0
            
            input = os.read(fdIn, 10000)
            if len(input) == 0:
                print("empty input file")
                return

            lines = re.split(b"\n", input)
            for line in lines:
                strToPrint = f"{line.decode()}\n"
                new_args = strToPrint.split()
                for arg in new_args:
                    args.insert(list_counter, arg)
                    list_counter += 1
        
        for dir in re.split(":", os.environ['PATH']):
            
            program = "%s/%s" % (dir, args[0])
    
            try:
                os.execve(program, args, os.environ)
                
            except FileNotFoundError: 
                pass 

        print(args[0]+": command not found")
        sys.exit(1)

    else:
        #os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %  (pid, rc)).encode())
        childPidCode = os.wait()
        #os.write(1, ("Parent: Child %d terminated with exit code %d\n" %  childPidCode).encode())

def main():
    intro()
    print("Welcome to Sergio Shell! Enter your command or 'exit' to terminate")
    
    user_command = get_user_command()

    while (user_command.lower() != "exit"):
        user_args = user_command.split()
        
        if user_args.count('cd') > 0:
            new_dir = user_args[user_args.index("cd") + 1]
            
            try:
                os.chdir(new_dir)
                os.write(1, (os.getcwd()+" \n").encode())
            except FileNotFoundError:
                os.write(1, (new_dir+" not found\n").encode())

            user_command = get_user_command()
            continue
        
    
        shell(user_args)

        user_command = get_user_command()

    print("Thank you for using my shell!")

if __name__ == "__main__":
    main()
