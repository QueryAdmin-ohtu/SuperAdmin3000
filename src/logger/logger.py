from datetime import datetime
import os


class Logger:
    """ A class for creating and reading logs of user operations
    """

    def __init__(self, username="ANONYMOUS", filename="superadmin.log"):

        self.username = username
        self.filename = filename

    def log_post_request(self, request):
        """ Write the request to the log, if the requst contains string "POST

        Returns:
            String: The log entry in success, None in failure.        
        """

        if request.method != "POST":
            return

        # Remove sensitive data
        form_values = {
            k: v for (k, v) in request.form.items() if "token" not in k}

        return self.write(f"POST:{request.path} FORM:{form_values}")

    def write(self, message, type="EVENT"):
        """
        Adds an event of type to the log with current time stamp

        Args:
            message: Text to be logged
            type: Type of the event
        Returns:
            String: The log entry in success, None in failure.

        """

        return self._write(datetime.now(), self.username, message, event_type="EVENT")

    def _write(self, time, user, message, event_type):
        """
        Adds an event of type to the log with current time stamp

        Args:
            time: Timestamp
            user: Username
            message: Text to be logged
            type: Type of the event("EVENT", "ERROR")
        Returns:
            String: The log entry in success, None in failure.
        """
        date_string = time.strftime("%Y-%m-%d %H:%M:%S")

        log_string = f"[{event_type}] {date_string} {user} {message}"

        try:
            with open(self.filename, "a") as f:
                f.write(log_string + '\n')
        except IOError:
            return None

        return log_string

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
        except IOError:
            return False

        return True
