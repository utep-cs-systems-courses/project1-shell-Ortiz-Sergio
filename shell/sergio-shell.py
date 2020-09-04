import os, sys, time, re

def my_shell():
    pid = os.getpid()

    os.write(1, ("About to fork (pid:%d)\n" %pid).encode())

    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:
        os.write(1, ("I am child. My pid=%d. Parent's pid=%d\n" % (os.getpid(), pid)).encode())
    else:
        os.write(1, ("I am parent. My pid=%d. Child's pid=%d\n" % (pid, rc)).encode())

def test():
    print("test print")


print("Welcome to this amazing shell! Enter your command or -1 to exit")
user_input = input("$ ")

while(user_input != '-1'):
    my_shell()
    user_input = input("$ ")

print("Thank you for using this amazing shell!")
