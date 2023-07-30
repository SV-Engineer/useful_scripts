######################################################################
#  Author: Austin | @SV-Engineer
#    Date: 22JUL2023
#
# Purpose: This script is for logging information to the console.
#
######################################################################

import datetime
from multiprocessing import Process, Lock

START_SECTION_WIDTH = 80
DELIMITER           = "=" * START_SECTION_WIDTH
START_MSG           = "module - {} - {}, {}"
INFO_MSG            = "*INFO: module - {} - {}, {}"
WARN_MSG            = "*WARN: module - {} - {}, {}"
ERR_MSG             = "**ERR: module - {} - {}, {}"

######################################################################
# BEGIN - Class Definitions
######################################################################
class Console:
  '''
  The purpose of this class is to provide verbose logging to the console. There are three
  types of logging: Informational, Warnings, and Errors. The StartSection method is considered
  informational. The reporting of these (with the exception of StartSection) may be turned on
  and off with the "Disable*" methods. Turning off the reporting does not disable the mechanism
  of counting how many warnings and errors that occur.
  '''
  def __init__(self, name: str) -> None:
    # All Logging is enabled by default
    self.__en_info       = True
    self.__en_warn       = True
    self.__en_err        = True
    self.__warning_count = 0
    self.__error_count   = 0
    self.__name          = name
  '''
  The following 3 methods disable the related logging to the console.
  '''
  def disable_info(self) -> None:
    self.__en_info = False

  def disable_warn(self) -> None:
    self.__en_warn = False

  def disable_err(self) -> None:
    self.__en_err  = False

  '''
  The following three methods enable the logging of the relavent
  kind to the console.
  '''
  def enable_info(self) -> None:
    self.__en_info = True

  def enable_warn(self) -> None:
    self.__en_warn = True

  def enable_err(self) -> None:
    self.__en_err  = True

  '''
  This private method is used for attaching a time stamp to the messages
  that are output to the console.
  '''
  def __get_time(self) -> str:
    # use the datetime module to get the current date, hour, minute and second.
    current_time = datetime.datetime.now()

    # Time extraction using 24-hour format.
    time = current_time.strftime("%H:%M:%S")

    # Date Extraction
    # Extract the month so it can be capitalized.
    month = current_time.strftime("%b")
    # Insert the abbreviated month in between the day and year
    date = current_time.strftime("%d{}%Y".format(month.upper()))

    # Return the Formatted date and time
    return "{} on {}".format(time, date)

  '''
  This method is used to indicate the start of a new test phase.
  '''
  def start_section(self, message: str) -> None:
    current_time = self.__get_time()
    msg          = START_MSG.format(self.__name, message, current_time)
    print("\n")
    print(DELIMITER)
    print(msg)
    print(DELIMITER)
    print("\n")

  '''
  This method is for providing informational messages to the console.
  '''
  def info(self, information: str) -> None:
    if (self.__en_info):
      current_time = self.__get_time()
      msg          = INFO_MSG.format(self.__name, information, current_time)
      print(msg)

    else:
      pass

  '''
  This method is for reporting warnings.
  '''
  def w(self, warning: str) -> None:
    self.__warning_count += 1
    if (self.__en_warn):
      current_time = self.__get_time()
      msg = WARN_MSG.format(self.__name, warning, current_time)
      print(msg)

    else:
      pass

  '''
  This method is for reporting errors.
  '''
  def e(self, error: str) -> None:
    self.__error_count += 1
    if (self.__en_err):
      current_time = self.__get_time()
      msg = ERR_MSG.format(self.__name, error, current_time)
      print(msg)

    else:
      pass

  '''
  This method is for showing the error and warning counts and reporting if the test passed or failed.
  '''
  def dump_counts(self) -> None:
    current_time = self.__get_time()
    print("\n")
    print("Printing Statistics, {}".format(current_time))
    print("    * Number of Warnings: {}".format(self.__warning_count))
    print("    * Number of   Errors: {}".format(self.__error_count))
    if (self.__error_count > 0):
      print("\nTest Failed!!!")

    else:
      print("\nTest Passed!!!")
    print("\n")

# endclass : Console

class Console_Threaded(Console):
  '''
  The purpose of this class is to extend the Console class to be
  enabled to function properly in the use case of threading. This
  class overrides all of the methods contained within the Console
  class and uses the "Super" keyword to wrap them in a mutex. The
  idea is that the "start_section" method can print all of its
  information without another thread interrupting. This directly
  implies new methods may be written to output multiple lines
  of data as well; such as a table of values.
  '''
  # A "static" lock is needed. The intent is that all class instances
  # share the following lock such that it is used as a mutex.
  lock_console = Lock()
  def __init__(self, name: str) -> None:
    super().__init__(name)

######################################################################
# END - Class Definitions
######################################################################

def main():
  console = Console("test_module")
  console.start_section("This is a test of the Console Class")
  console.info("This is an informational message")
  console.w("This is a warning messge")
  console.e("This is an error message")
  console.dump_counts()

if __name__ == "__main__":
  main()
