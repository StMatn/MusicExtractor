# MusicExtractor
Tool for extracting passages from long audio files.

## Notes
* Audacity must be running before executing the script.
* Audacity may crash on close after the script is executed.

## Usage

### Time list
Provide one passage to be cut out per line.

Syntax for passages: \<start_time\>-\<end_time\>

Syntax for \<start_time\> and \<end_time\>: \[\<number\>:\]*\<number\> where the rightmost number represents seconds. The place value of each additional \<number\>: is 60 times the place value to its right.

### Arguments
Providing no arguments will print the help text.

Provide arguments in the format \<argument\>=\<value\>. You can provide multiple arguments separated by spaces.

Argument | Description | Default value
-------- | ----------- | -------------
default | Run program with default settings. Omit "=\<value\>". | n/a
input | Specify input file from current working directory | input.mp3
inputFilePath | Specify absolute location of input file. | \<working directory\> + \<input\>
outputPrefix | Pfefix of output files. Two-digit running number is added to parts. | output-
outputDirectoryName | Name of directory for output files. Directory will be created in current working directory. | output
outputDirectoryPath | Specify absolute path of directory for output files. No subdirectory will be created! | \<working directory\> + \<outputDirectoryName\>
