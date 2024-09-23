import os
import sys
from time import sleep
import re


###################################
########## Program usage ##########
###################################


def printHelp():
    print("========== Help ==========")
    print("=== Usage ===")
    print("Add argument list:")
    print("    <argument>=<value>")
    print("=== Input times ===")
    print("    Create \"times.txt\" in working directory")
    print("    Add track times line by line in format <startTime>-<endTime>")
    print("    <startTime> and <endTime> have format [[hours:]minutes:]seconds")
    print("=== Arguments ===")
    print("    default: Run program with default settings.")
    print("        Ommit \"=<value>\"")
    print("    input: Specify input file from current working directory.")
    print("        Default value: input.mp3")
    print("    inputFilePath: Specify absolute location of input file.")
    print("        Default value: <working directory> + <input>")
    print("    outputPrefix: Pfefix of output files. Two-digit running number is added to parts.")
    print("        Default value: output-")
    print("    outputDirectoryName: Name of directory for output files. Directory will be created in current working directory.")
    print("        Default value: output")
    print("    outputDirectoryPath: Specify absolute path of directory for output files. No subdirectory will be created!")
    print("        Default value: <working directory> + <outputDirectoryName>")


if len(sys.argv) == 1 or sys.argv[1] == "help":
    printHelp()
    sys.exit()

####################################
########## Audacity stuff ##########
####################################
audacityCommandAcceptorPath = ""
audacityResponsePath = ""
lineDelimiter = ""
dirDelimiter = ""

# set paths respective to OS variant
if sys.platform == 'win32':
    audacityCommandAcceptorPath = "\\\\.\\pipe\\ToSrvPipe"
    audacityResponsePath = "\\\\.\\pipe\\FromSrvPipe"
    lineDelimiter = "\r\n\0"
    dirDelimiter = "\\"
else:
    audacityCommandAcceptorPath = "/tmp/audacity_script_pipe.to." + str(os.getuid())
    audacityResponsePath = "/tmp/audacity_script_pipe.from." + str(os.getuid())
    lineDelimiter = "\n"
    dirDelimiter = "/"

print("=== Connecting to Audacity ... ===")

if not os.path.exists(audacityCommandAcceptorPath):
    print("Error connecting to Audacity: Pipe not found. Is Audacity running and scripting enabled?")
    sys.exit()

# Apparent race condition in Audacity -> Sleep to ensure Audacity is available for next command
sleep(.1)

if not os.path.exists(audacityResponsePath):
    print("Error connecting to Audacity: Pipe not found. Is Audacity running and scripting enabled?")
    sys.exit()

# Apparent race condition in Audacity -> Sleep to ensure Audacity is available for next command
sleep(.1)

audacityCommandAcceptor = open(audacityCommandAcceptorPath, 'w')

# Apparent race condition in Audacity -> Sleep to ensure Audacity is available for next command
sleep(.1)

audacityResponder = open(audacityResponsePath, 'rt')

print("=== Connection to Audacity established ===")


def sendCommand(command):
    audacityCommandAcceptor.write(command + lineDelimiter)
    audacityCommandAcceptor.flush()


def readResponse():
    response = ''
    line = ''
    while True:
        response += line
        line = audacityResponder.readline()
        if line == '\n' and len(response) > 0:
            break
    return response


def executeCommand(command, printResponse=False):
    sendCommand(command)
    response = readResponse()
    if (printResponse):
        print("AudacityResponse: " + response)
    return response


###################################
########## Cutting stuff ##########
###################################

# === input file stuff ===
inputFileName = "input.mp3"
inputFileDir = os.path.abspath(os.getcwd())
inputFilePath = inputFileDir + dirDelimiter + inputFileName

# === output file stuff ===
outputPrefix = "output-"
outputFolderName = "output"
outputFolderDir = os.path.abspath(os.getcwd())
outputFolderPath = outputFolderDir + dirDelimiter + outputFolderName + dirDelimiter

# === driver code ===
songNumber = 1


def convertTimeToSeconds(timestamp):
    parts = timestamp.split(":")
    seconds = int(parts[0])
    for x in parts[1:]:
        seconds *= 60
        seconds += int(x)
    return seconds


def sendCuttingCommands():
    global inputFilePath

    global outputPrefix
    global outputFolderPath

    global songNumber

    print("=== Current settings ===")

    print("Input file:")
    print("    " + inputFilePath)

    print("Output directory:")
    print("    " + outputFolderPath)

    print("Output prefix:")
    print("    " + outputPrefix)

    print("=== Starting cutting process ===")

    # open
    executeCommand('OpenProject2: Filename="' + inputFilePath + '"')

    # check output dir
    if not os.path.isdir(outputFolderPath):
        os.makedirs(outputFolderPath)

    # open time input file
    timeInputFile = open("times.txt", "rt")

    # extract tracks
    line = timeInputFile.readline()
    while line != "":
        parts = line.split("-")
        executeCommand('SelectTime: Start=' + str(convertTimeToSeconds(parts[0])) + ' End=' + str(convertTimeToSeconds(parts[1])))
        executeCommand('Export2: Filename="' + outputFolderPath + outputPrefix + ("0" if songNumber < 10 else "") + str(songNumber) + '.mp3"')
        songNumber += 1
        line = timeInputFile.readline()

    # close on finish
    executeCommand('TrackClose:')

    print("=== Finished ===")
    print("Enjoy your separated files")


# === main program ===
# parse arguments
print("=== Parsing arguments ===")
for arg in sys.argv[1:]:
    parts = arg.split("=")
    match parts[0]:
        case "default":
            pass
        case "input":
            inputFileName = parts[1]
            inputFilePath = inputFileDir + dirDelimiter + inputFileName
        case "inputFilePath":
            inputFilePath = parts[1]
        case "outputPrefix":
            outputPrefix = parts[1]
        case "outputDirectoryName":
            outputFolderName = parts[1]
            outputFolderPath = outputFolderDir + dirDelimiter + outputFolderName + dirDelimiter
        case "outputDirectoryPath":
            outputFolderPath = parts[1]
        case "partLength":
            partLength = int(parts[1])
        case "minPartLength":
            minPartLength = int(parts[1])
        case _:
            print("Error reading arguments: Argument unknown: " + parts[0])
            printHelp()
            sys.exit()


# run cutting code
sendCuttingCommands()
