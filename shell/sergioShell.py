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
        time.sleep(1)
        os.write(1, "Child  ....terminating now with exit code 0\n".encode())
        sys.exit(0)
    else:
        os.write(1, ("I am parent. My pid=%d. Child's pid=%d\n" % (pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" %childPidCode).encode())

def main() :
    print("Welcome to Sergio Shell! Type in your command or 'exit' to terminate")
    user_command = input("$ ")

    while(user_command != "exit"):
        my_shell()
        user_command = input("$ ")

    print("Thank you for using my shell!")

if __name__ == "__main__":
    main()
