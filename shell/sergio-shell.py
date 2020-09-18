#! /usr/bin/env python3

import os, sys, time, re

def main():
    while True:
        user_args = get_user_args()

        if 'cd' in user_args:
            try:
                os.chdir(user_args[1])
            except FileNotFoundError:
                pass

            continue

        if 'exit' in user_args:
            sys.exit(0)

        if '&' in user_args:
            user_args.remove('&')

        if len(user_args) == 0:
            pass
    
        my_shell(user_args)

def get_user_args():
    if 'PS1' in os.environ:
        os.write(1, (os.environ['PS1']).encode())
    else:
        os.write(1, ('$ ').encode())
    try:
        args = [str(n) for n in input().split()]
    except EOFError:
        sys.exit(1)
        
    return args

def my_shell(args):
    pid = os.getpid()

    rc = os.fork()

    if rc < 0:
        sys.exit(1)

    elif rc == 0:
        if '>' in args:
            os.close(1)
            os.open(args[-1], os.O_CREAT | os.O_WRONLY);
            os.set_inheritable(1, True)
            execute(args[0: args.index('>')])

        elif '<' in args:
            os.close(0)
            os.open(args[-1], os.O_RDONLY)
            os.set_inheritable(0, True)
            execute(args[0: args.index('<')])

        elif '|' in args:
            pipe(args)

        elif '/' in args[0]:
            cur_program = args[0]
            try:
                os.execve(cur_program, args, os.environ)
            except FileNotFoundError:
                pass

        else:
            execute(args)

    else:
        childPidCode = os.wait()

def execute(args):
    for dir in re.split(":", os.environ['PATH']):
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ)
        except FileNotFoundError:
            pass
    os.write(2, (f"{args[0]}: command not found.\n").encode())
    sys.exit(1)

def pipe(args):
    pipe1 = args[0:args.index('|')]
    pipe2 = args[args.index('|')+1:]

    pr, pw = os.pipe()
    for f in (pr, pw):
        os.set_inheritable(f, True)

    rc = os.fork()
    if rc < 0:
        sys.exit(1)

    elif rc == 0:
        os.close(1)
        os.dup(pw) #route fd1 to pipe input
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

        if '|' in pipe2:
            pipe(pipe2)
        
        execute(pipe2)

if __name__ == "__main__":
    main()
