######################################################################
#  Author: Austin | @SV-Engineer
#    Date: 22JUL2023
#
# Purpose: This script is for renaming music files to a consistent
#          format rather than the various non-standardized formats
#          they come in off of CDs.
#
# Warning: Checking if the desired format is already the name is not
#          implemented. Behavior unverified and will likely throw an
#          index out of range error when using the SUB_STR_IDX variable.
#
######################################################################

import os
import sys
import re as regex
from argparse import ArgumentParser
from argparse import Namespace

# The pattern that comes up most often. TODO: create a file of all of the common patterns.
RE_PATTERN  = "((\d+) (.+\.mp3))"
# The split function from the regex module returns the original string, followed by the captured
# substrings as denoted by the parenthesis.
SUB_STR_IDX = 1

def get_cmd_line_args() -> Namespace:
  '''
  The purpose of this function is to add command line functionality to the script so that the script
  itself does not need to be stored in the same directory as the music files.
  TODO: Add the recursive functionality.
  '''
  ap = ArgumentParser("Directory to run this script on")
  ap.add_argument("-d", type=str,  default=None, required=False, help="If a string to a directory is passed, absolute or relative, this script will operate there. Otherwise it operates on the cwd.")
  ap.add_argument("-r", type=bool, default=None, required=False, help="[Unimplemented Feature] If passed, the script will interact recursively.")

  return ap.parse_args()

def get_file_names() -> list:
  '''
  The purpose of this function is to retrieve file names from the current directory. An empty list will
  be returned instead if no files with the correct extension are found.
  TODO: Add other extensions such as wav, wma, etc.
  '''
  file_names       = os.scandir()
  music_file_names = []
  for f in file_names:
    tmp = str(f.name)

    if (tmp.endswith(".mp3")):
      music_file_names.append(tmp)

    else:
      pass

  return music_file_names

def rename_mp3_files(file_names: list) -> None:
  '''
  The purpose of this function is to rename the files to the desired format.
  TODO: Add checking to ensure the original name is not already in the desired
  format.
  '''
  sub_string = ""
  new_name = ""
  for name in file_names:
    sub_string = regex.split(RE_PATTERN, name, 1)
    if ((sub_string[SUB_STR_IDX + 1] != '') and (sub_string[SUB_STR_IDX + 2] != '')):
      new_name = "{} - {}".format(sub_string[SUB_STR_IDX + 1], sub_string[SUB_STR_IDX + 2])
      print(new_name)
      os.rename(name, new_name)
      sub_string = ""
      new_name = ""

    else:
      print("Warning, A file was missed, {}.".format(name))

def perform_rename_steps() -> None:
  '''
  This function consolidates the steps for renaming the files
  to accomodate for the possibilities of command line switches
  or no command line switches being passed without repeating
  more than one line of code.
  '''
  f_names = get_file_names()
  # Empty lists evaluate to false
  if (f_names):
    rename_mp3_files(file_names=f_names)

  else:
    pass

def perform_rename_diff_dir(dir: str) -> None:
  '''
  This function consolidates the steps for renaming the files
  and the steps of changing directories.
  '''
  # Save Current directory for later.
  current_directory = os.getcwd()
  os.chdir(str(dir))

  # Perform rename operation(s).
  perform_rename_steps()

  # Change back to the original directory.
  os.chdir(current_directory)

def main():
  '''
  Main entry point in the event this script is called directly
  instead of as an import.
  '''
  # No Arguments have been passed.
  if not len(sys.argv) > 1:
    # Perform rename operation(s).
    perform_rename_steps()

  # Arguements have been passed.
  else:
    args = get_cmd_line_args()

    # TODO: Implement path for recursive operation & different directory switch.
    if (args.d is not None) and (args.r is not None):
      pass

    # Only changing directory, no recursion.
    elif args.d is not None:
      perform_rename_diff_dir(args.d)

    # TODO: Add recursive steps here.
    else:
      pass


if __name__ == "__main__":
  main()