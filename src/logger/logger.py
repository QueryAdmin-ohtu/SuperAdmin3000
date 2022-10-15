from datetime import datetime
import os

class Logger:
    """ A class for creating and reading logs of user operations
    """

    def __init__(self, filename="superadmin.log"):
        self.filename = filename

    def write(self, user, message, type="EVENT"):
        """
        Adds an event of type to the log with current time stamp

        Args:
            user: Username
            message: Text to be logged
            type: Type of the event("EVENT", "ERROR")
        Returns:
            Boolean (True if write was successfull)
       
        """
        return self._write(datetime.now(), user, message, event_type="EVENT")
        
    def _write(self, time, user, message, event_type):
        """
        Adds an event of type to the log with current time stamp

        Args:
            time: Timestamp
            user: Username
            message: Text to be logged
            type: Type of the event("EVENT", "ERROR")
        Returns:
            Boolean (True if write was successfull)
       
        """

        log_string = f"[{event_type}] {time} {user} {message}"

        try:
            with open(self.filename, "a") as f:
                f.write(log_string)
        except IOError:
            return False

        return True
            
    def read_all_events(self):
        """
        Reads event log from a file and returns an array
        containing every line, or Null if error happens 

        Returns:
            An array of strings
        """

        try:
            with open(self.filename, "r") as f:
                lines = f.readlines()
        except IOError:
            return None

        return lines

    def _delete_log(self):
        """
        Delete the log file
        """

        try:
            os.remove(self.filename)
        except:
            return False

        return True
        

