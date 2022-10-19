from datetime import datetime
import os


class Logger:
    """ A class for creating and reading logs of user operations
    """

    def __init__(self,
                 username="ANONYMOUS",
                 filename="superadmin.log",
                 log_requests=["POST"],
                 sensitive=["token", "password", "credential"]
    ):

        self.username = username
        self.filename = filename
        self.log_requests = log_requests
        self.sensitive = sensitive

    def log_post_request(self, request):
        """ Write the request to the log, if the requst contains string found in
        the log_requests array and is not sensitive data

        Returns:
            String: The log entry in success, None in failure.
        """

        if request.method not in self.log_requests:
            return

        # Remove sensitive data which should not be written in the log
        form_dict = {}
        
        for (key, value) in request.form.items():
            sensitive_field = False
            for s in self.sensitive:
                if s in key:
                    sensitive_field = True
                    break
            if not sensitive_field:
                form_dict[key] = value

        form_string = self.prettify(form_dict)
        
        return self.write(
            f"{request.path}{form_string}",
            event_type=request.method
        )

    def prettify(self, form):
        """ Format given form to printable form

        Arguments:
            Form dictionary
        Returns:
            String
        """

        return_string = "\n"

        for (key, value) in form.items():
            return_string += f"{'':<5}{key:<20}{value}\n"

        return return_string
    
    def write(self, message, event_type="EVENT"):
        """
        Adds an event of type to the log with current time stamp

        Args:
            message: Text to be logged
            event_type: Type of the event, such as POST or GET
        Returns:
            String: The log entry in success, None in failure.

        """

        return self._write(datetime.now(), self.username, message, event_type)

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
            with open(self.filename, "a") as file:
                file.write(log_string + '\n')
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
            with open(self.filename, "r") as file:
                lines = file.readlines()
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
