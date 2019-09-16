# Register values:
WRITEDAC         = 0x40
WRITEDACEEPROM   = 0x60

from smbus2 import SMBus

class MCP4725(object):
    """Base functionality for MCP4725 digital to analog converter."""

    def __init__(self, address):
        """Create an instance of the MCP4725 DAC."""
        self._device = SMBus(1)
        self._address = address

    def set_voltage(self, value, persist=False):
        """Set the output voltage to specified value.  Value is a 12-bit number
        (0-4095) that is used to calculate the output voltage from:

          Vout =  (VDD*value)/4096

        I.e. the output voltage is the VDD reference scaled by value/4096.
        If persist is true it will save the voltage value in EEPROM so it
        continues after reset (default is false, no persistence).
        """
        # Clamp value to an unsigned 12-bit value.
        if value > 4095:
            value = 4095
        if value < 0:
            value = 0
        
        reg_data = [(value >> 4) & 0xFF, (value << 4) & 0xFF]
        
        if persist:
            self._device.write_block_data(self._address, WRITEDACEEPROM, reg_data)
        else:
            self._device.write_block_data(self._address, WRITEDAC, reg_data)
