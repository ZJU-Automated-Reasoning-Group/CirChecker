from antlr4 import *
import subprocess
import sys
import os

sys.path.append('./test/')

# Make sure that ANTLR_JAR is set to antlr-4.9.2-complete.jar
ANTLR_JAR = os.environ.get('ANTLR_JAR')
TARGET = '../target/main/Circom/parser' if os.name == 'posix' else os.path.normpath(
    '../target/')


def main(argv):
    global ANTLR_JAR, TARGET
    if len(argv) < 1:
        printUsage()
    elif argv[0] == 'gen':
        subprocess.run(["java", "-jar", ANTLR_JAR, "-o", "./circheck/target",
                        "-no-listener", "-visitor", "circheck/parser/Circom.g4"])
    else:
        printUsage()


def printUsage():
    print("python3 run.py gen")


if __name__ == "__main__":
    main(sys.argv[1:])
