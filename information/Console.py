import datetime

START_SECTION_WIDTH = 80
DELIMITER           = "=" * START_SECTION_WIDTH
START_MSG           = "module - {} - {}, {}"
INFO_MSG            = "*INFO: module - {} - {}, {}"
WARN_MSG            = "*WARN: module - {} - {}, {}"
ERR_MSG             = "**ERR: module - {} - {}, {}"

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
    self.__enInfo       = True
    self.__enWarn       = True
    self.__enErr        = True
    self.__warningCount = 0
    self.__errorCount   = 0
    self.__name         = name
  '''
  The following 3 methods disable the related logging to the console.
  '''
  def DisableInfo(self) -> None:
    self.__enInfo = False

  def DisableWarn(self) -> None:
    self.__enWarn = False

  def DisableErr(self) -> None:
    self.__enErr  = False

  '''
  The following three methods enable the logging of the relavent
  kind to the console.
  '''
  def EnableInfo(self) -> None:
    self.__enInfo = True

  def EnableWarn(self) -> None:
    self.__enWarn = True

  def EnableErr(self) -> None:
    self.__enErr  = True

  '''
  This private method is used for attaching a time stamp to the messages
  that are output to the console.
  '''
  def __getTime(self) -> str:
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
  def StartSection(self, message: str) -> None:
    current_time = self.__getTime()
    msg          = START_MSG.format(self.__name, message, current_time)
    print("\n")
    print(DELIMITER)
    print(msg)
    print(DELIMITER)
    print("\n")

  '''
  This method is for providing informational messages to the console.
  '''
  def Info(self, information: str) -> None:
    if (self.__enInfo):
      current_time = self.__getTime()
      msg          = INFO_MSG.format(self.__name, information, current_time)
      print(msg)

    else:
      pass

  '''
  This method is for reporting warnings.
  '''
  def W(self, warning: str) -> None:
    self.__warningCount += 1
    if (self.__enWarn):
      current_time = self.__getTime()
      msg = WARN_MSG.format(self.__name, warning, current_time)
      print(msg)

    else:
      pass

  '''
  This method is for reporting errors.
  '''
  def E(self, error: str) -> None:
    self.__errorCount += 1
    if (self.__enErr):
      current_time = self.__getTime()
      msg = ERR_MSG.format(self.__name, error, current_time)
      print(msg)

    else:
      pass

  '''
  This method is for showing the error and warning counts and reporting if the test passed or failed.
  '''
  def DumpCounts(self) -> None:
    current_time = self.__getTime()
    print("\n")
    print("Printing Statistics, {}".format(current_time))
    print("    * Number of Warnings: {}".format(self.__warningCount))
    print("    * Number of   Errors: {}".format(self.__errorCount))
    if (self.__errorCount > 0):
      print("\nTest Failed!!!")
    print("\n")

console = Console("test_module")

def main():
  console.StartSection("This is a test of the Console Class")
  console.Info("This is an Informational message")
  console.W("This is a warning messge")
  console.E("This is an error message")
  console.DumpCounts()

if __name__ == "__main__":
  main()
