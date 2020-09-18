#! /usr/bin/env python3

import os, sys, time, re

def execute(args):
    for dir in re.split(":", os.environ['PATH']):
        program = "%s/%s" % (dir, args[0])

        try:
            os.execve(program, args, os.environ)
        except FileNotFoundError:
            pass

    sys.exit(1)

def get_user_command():
    if 'PS1' in os.environ:
        os.write(1, (os.environ['PS1']).encode())
        try:
            args = [str(n) for n in input().split()]
        except EOFError:
            sys.exit()
    else:
        try:
            args = [str(n) for n in input().split()]
        except EOFError:
            sys.exit(1)
    return args
            

def shell(args):
    output_redirect = False
    input_redirect = False

    if args.count(">") > 0:
        output_redirect = True
        output_file = args[args.index(">") + 1]
        args.remove(">")
        args.remove(output_file)

    if args.count("<") > 0:
        input_redirect = True
        input_file = args[args.index("<") - 1]

    if '&' in args:
        args.remove('&')        

    pid = os.getpid()
    
    rc = os.fork()
    
    if rc < 0:
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
                return

            lines = re.split(b"\n", input)
            for line in lines:
                strToPrint = f"{line.decode()}\n"
                new_args = strToPrint.split()
                for arg in new_args:
                    args.insert(list_counter, arg)
                    list_counter += 1

        if "|" in args:
            args = ' '.join([str(elem) for elem in args])
            pipe = args.split("|")
            pipe1 = pipe[0].split()
            pipe2 = pipe[1].split()

            pr, pw = os.pipe()
            for f in (pr, pw):
                os.set_inheritable(f, True)

            pipeFork = os.fork()
            
            if pipeFork < 0:
                sys.exit(1)

            elif pipeFork == 0:
                os.close(1)
                os.dup(pw)
                os.set_inheritable(1, True)
                for fd in (pr, pw):
                    os.close(fd)
                execute(pipe1)

            else:
                os.close(0)
                os.dup(pr)
                os.set_inheritable(0, True)
                for fd in (pw, pr):
                    os.close(fd)
                execute(pipe2)

            return
        
        execute(args)

    else:
        childPidCode = os.wait()

def main():
    user_args = get_user_command()

    while not('exit' in user_args):
        
        if user_args.count('cd') > 0:
            try:
                os.chdir(user_args[1])
            except FileNotFoundError:
                pass

            user_args = get_user_command()
            continue
        
        shell(user_args)

        user_args = get_user_command()

if __name__ == "__main__":
    main()
