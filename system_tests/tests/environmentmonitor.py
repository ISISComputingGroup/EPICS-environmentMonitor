import unittest
from parameterized import parameterized

from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc, skip_if_recsim, parameterized_list


DEVICE_PREFIX = "ENVMON_01"


IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("ENVMON"),
        "macros": {},
        "emulator": "Envmon",
    },
]


TEST_MODES = [TestModes.RECSIM, TestModes.DEVSIM]


class EnvironmentmonitorTests(unittest.TestCase):
    """
    Tests for the Environmentmonitor IOC.
    """
    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("Envmon", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX)

    def test_WHEN_ioc_started_THEN_ioc_is_not_disabled(self):
        self.ca.assert_that_pv_is("DISABLE", "COMMS ENABLED")

    @skip_if_recsim
    def test_GIVEN_tempA_on_device_20_THEN_ioc_reports_20(self):
        # Force Emulator to have a tempA 20
        
        self._lewis.backdoor_set_on_device("temperature", 20)
        self.ca.assert_that_pv_is_number("TEMPA", 20, tolerance=0.01)

    @skip_if_recsim
    def test_GIVEN_tempB_on_device_30_THEN_ioc_reports_30(self):
        # Force Emulator to have a tempB 30
        
        self._lewis.backdoor_set_on_device("temperature", 30)
        self.ca.assert_that_pv_is_number("TEMPB", 30, tolerance=0.01)

    @parameterized.expand(parameterized_list(["TEMPA", "TEMPB"]))
    @skip_if_recsim
    def test_WHEN_device_disconnects_THEN_pvs_go_into_alarm(self, _, pv):
        self.ca.assert_that_pv_alarm_is(pv, self.ca.Alarms.NONE)

        with self._lewis.backdoor_simulate_disconnected_device():
            self.ca.assert_that_pv_alarm_is(pv, self.ca.Alarms.INVALID, timeout=30)

        self.ca.assert_that_pv_alarm_is(pv, self.ca.Alarms.NONE, timeout=30)