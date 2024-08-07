from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply

if_connected = conditional_reply("connected")

# Devsim device Functionality


@has_log
class EnvmonStreamInterface(StreamInterface):
    in_terminator = "\r"
    out_terminator = "\r"

    def __init__(self):
        super(EnvmonStreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {CmdBuilder(self.get_status).escape("?STS").build()}

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    @if_connected
    def get_status(self):
        # e.g "A21.31,B43.01,C22.12,D31.67"
        return f"A{self.device.temperatureA},B{self.device.rhumidityA},C{self.device.temperatureB},D{self.device.rhumidityB}"
