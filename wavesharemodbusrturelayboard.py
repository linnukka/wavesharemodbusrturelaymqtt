#!/usr/bin/python
# coding=utf_8
#

import json
import pytz
from datetime import datetime
from pymodbus.client import ModbusSerialClient
from pymodbus.register_read_message import ReadHoldingRegistersResponse
from pymodbus.bit_read_message import ReadCoilsResponse
from pymodbus.bit_write_message import WriteMultipleCoilsResponse, WriteSingleCoilResponse
from pymodbus.register_write_message import WriteSingleRegisterResponse

#from pymodbus import ModbusIOException

class WaveshareModbusRtuRelayBoard:

    client = None
    logger = None
    modbusAddress = None
    relaystates = None

    coilsDict = {
        "relayboard_name" : None,
        "modbus_address" : None,
        "time" : None,
        "UTC_time" : None,
        "Relay1" : None,
        "Relay2" : None,
        "Relay3" : None,
        "Relay4" : None,
        "Relay5" : None,
        "Relay6" : None,
        "Relay7" : None,
        "Relay8" : None
    }

    # Assumes that client has been connected! 
    def __init__(self, modbusClient, modbusAddress, relayboardName, logger):
        logger.debug("Initializing: Modbus unit %d, board: %s", modbusAddress, relayboardName)
        self.client = modbusClient
        self.modbusAddress = modbusAddress
        self.logger = logger
        self.relayboardName = relayboardName

    def getINT32(self, lowword, highword):
        # self.logger.debug("getINT32: %d, %d", lowword, highword)
        return int((highword << 16) | lowword)

    def cleanup(self):
        client.close()

    def getrelayboardName(self):
        return self.relayboardName

    def readRelays(self):
        self.logger.debug("Relays %s reading starts, unit number %d", self.relayboardName, self.modbusAddress)

        response = self.client.read_coils(0x00, 0x08, unit=self.modbusAddress)

        if((response is not None) and (isinstance(response, ReadCoilsResponse))):
            #self.logger.debug("Got response, parsing instaneous values")

            self.coilsDict = {
                "relayboard_name" : self.relayboardName,
                "modbus_address" : self.modbusAddress,
                "time" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "UTC_time" :  datetime.utcnow().replace(tzinfo=pytz.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "CH1" : int(response.bits[0]),
                "CH2" : int(response.bits[1]),
                "CH3" : int(response.bits[2]),
                "CH4" : int(response.bits[3]),
                "CH5" : int(response.bits[4]),
                "CH6" : int(response.bits[5]),
                "CH7" : int(response.bits[6]),
                "CH8" : int(response.bits[7])
            }
            relaystates = [int(response.bits[0]), int(response.bits[1]), int(response.bits[2]), int(response.bits[3]), int(response.bits[4]),
                            int(response.bits[5]), int(response.bits[6]), int(response.bits[7])]
            self.logger.debug("Parsed. As JSON: " + json.dumps(self.coilsDict))
            self.logger.debug("Relaystates: %s", relaystates)
        else:
            self.logger.debug("Response None!")
            self.logger.debug(response)
        return json.dumps(self.coilsDict)

    def writeRelays(self, relayStates):
        self.logger.debug("Relays %s writing starts, unit number %d. States: %s", self.relayboardName, self.modbusAddress, relayStates)

        response = self.client.write_coils(0x00, relayStates, unit=self.modbusAddress)

        if((response is not None) and (isinstance(response, WriteMultipleCoilsResponse))):
            self.logger.debug("Got response!")
        else:
            self.logger.debug("Response None!")
            self.logger.debug(response)
        return

    def turnOnRelay(self, channelNumber):
        self.logger.debug("Turning on CH%d of %s. Unit number %d.", channelNumber, self.relayboardName, self.modbusAddress)

        response = self.client.write_coil(channelNumber-1, True, unit=self.modbusAddress)

        if((response is not None) and (isinstance(response, WriteSingleCoilResponse))):
            self.logger.debug("Got response!")
        else:
            self.logger.debug("Response None!")
            self.logger.debug(response)
        return

    def turnOffRelay(self, channelNumber):
        self.logger.debug("Turning off CH%d of %s. Unit number %d.", channelNumber, self.relayboardName, self.modbusAddress)

        response = self.client.write_coil(channelNumber-1, False, unit=self.modbusAddress)

        if((response is not None) and (isinstance(response, WriteSingleCoilResponse))):
            self.logger.debug("Got response!")
        else:
            self.logger.debug("Response None!")
            self.logger.debug(response)
        return

    def turnAllOff(self):
        self.logger.debug("Turning off all of %s. Unit number %d.", self.relayboardName, self.modbusAddress)

        response = self.client.write_coil(0x00FF, False, unit=self.modbusAddress)

        if((response is not None) and (isinstance(response, WriteSingleCoilResponse))):
            self.logger.debug("Got response!")
        else:
            self.logger.debug("Response None!")
            self.logger.debug(response)
        return

    def turnAllOn(self):
        self.logger.debug("Turning on all of %s. Unit number %d.", self.relayboardName, self.modbusAddress)

        response = self.client.write_coil(0x00FF, True, unit=self.modbusAddress)

        if((response is not None) and (isinstance(response, WriteSingleCoilResponse))):
            self.logger.debug("Got response!")
        else:
            self.logger.debug("Response None!")
            self.logger.debug(response)
        return

    def setBaudRate9600N(self):
        self.logger.debug("Setting baud rate to 9600N on %s. Unit number %d.", self.relayboardName, self.modbusAddress)

        response = self.client.write_register(0x2000, 0x0001, unit=self.modbusAddress)

        if((response is not None) and (isinstance(response, WriteSingleRegisterResponse))):
            self.logger.debug("Got response!")
        else:
            self.logger.debug("Response None!")
            self.logger.debug(response)
        return
