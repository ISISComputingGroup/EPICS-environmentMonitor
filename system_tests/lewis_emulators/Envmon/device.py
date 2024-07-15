from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice

# Devsim device

class SimulatedEnvmon(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        self.temperatureA = 0
        self.temperatureB = 0
        self.rhumidityA = 0
        self.rhumidityB = 0
        self.connected = True

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])
