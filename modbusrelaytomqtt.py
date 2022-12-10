#!/usr/bin/python
# coding=utf-8
#  pip3 install pytz paho-mqtt configparser pymodbus pyserial

import paho.mqtt.client as mqtt
import os
import ntpath
import shutil
import json
import threading
import time
from datetime import datetime
import pytz
import logging
import logging.config
# import RPi.GPIO as GPIO
import smtplib
import configparser
from queue import Queue
from wavesharemodbusrturelayboard import WaveshareModbusRtuRelayBoard

# --------------------------------------------------------------------------- #
# import the various client implementations
# --------------------------------------------------------------------------- #
from pymodbus.client import ModbusSerialClient 
from pymodbus.transaction import (ModbusAsciiFramer,ModbusRtuFramer)

if __name__ == '__main__':

    # CONFIG
    configParser = configparser.RawConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})
    configFilePath = '/home/j/scripts/modbusrelay/modbusrelay.conf'
    configParser.read(configFilePath)
    credConfigParser = configparser.RawConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]})
    credConfigFilePath = '/home/j/scripts/modbusrelay/mqtt_credentials.conf'
    credConfigParser.read(credConfigFilePath)

    log_level = configParser.get('LOGGER', 'logLevel')
    modbusclient = ModbusSerialClient(method=configParser.get('MODBUS', 'method'), 
                                port=configParser.get('MODBUS', 'port'), 
                                timeout=configParser.getint('MODBUS', 'timeout'), 
                                stopbits = configParser.getint('MODBUS', 'stopbits'), 
                                bytesize = configParser.getint('MODBUS', 'bytesize'),  
                                parity=configParser.get('MODBUS', 'parity'), 
                                baudrate=configParser.getint('MODBUS', 'baudrate'))
    confMqttClientName = configParser.get('MQTT', 'clientName')
    mqttQos = configParser.getint('MQTT', 'mqttQos')
    mqttRetain = configParser.getboolean('MQTT', 'mqttRetain')

    mqttc = mqtt.Client(confMqttClientName)

    logging.config.fileConfig(fname=configParser.get('LOGGER','loggerConfigFileName'), disable_existing_loggers=configParser.getboolean('LOGGER','disableExistingLoggers'))
    logger = logging.getLogger(configParser.get('LOGGER','mainLoggerName'))
    logger.setLevel(log_level)
    logger.info('Log level is %s', logging.getLevelName(logger.level))

    confSiteName = configParser.get('MQTT', 'siteName')
    confPubTopicPrefix = configParser.get('MQTT', 'pubTopicPrefix')
    confPubTopicStateSuffix = configParser.get('MQTT', 'pubTopicStateSuffix')
    confSubTopicPrefix = configParser.get('MQTT', 'subTopicPrefix')
    confCmdTopicSuffix = configParser.get('MQTT', 'cmdTopicSuffix')
    confRelayOnCommandPayload = configParser.get('MQTT', 'relayOnCommandPayload')
    confRelayOffCommandPayload = configParser.get('MQTT', 'relayOffCommandPayload')
    confRelayStatusCommandPayload = configParser.get('MQTT', 'relayStatusCommandPayload')


    logger.debug('----------------- starting modbus relay interface -----------------')

    # buffer of data to output to the serial port
    outputData = []

    cmdQueue = Queue()

    # Boards
    boardNames = configParser.getlist('MODBUS','boardNames')
    logger.debug('boardNames: ')
    logger.debug(boardNames)
    boards = []
    pubTopics = []

    for i in range(len(boardNames)):
        logger.debug('Adding board %s at pos %d', boardNames[i], i)
        
        boards.append(WaveshareModbusRtuRelayBoard(modbusclient, i+1, boardNames[i], logger))

        ### TODO
        # Publish topics structured as <siteName>/<pubTopicPrefix>/<board_name> (+ /CHx/state for individual states) 
        # CH1..8 and state will added on relevant publish 

        pubTopics.append("%s%s%s" % (confSiteName,confPubTopicPrefix,boardNames[i]))

    ####  MQTT callbacks
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
        #rc 0 successful connect
            logger.debug("Connected")
        else:
            raise Exception
        
        # subscribe to the MQTT cmd messages
        # Subscribe topics structured as <sitename>/<subTopicPrefix>/<board_name>/CHx/<cmdTopicSuffix>
        for i in range(len(boardNames)):

            subTopic = "%s%s%s%s%s" % (confSiteName, confSubTopicPrefix, boardNames[i], "/+", confCmdTopicSuffix)
            logger.debug("Subscribing to: %s", subTopic)                                 
            output_mid = client.subscribe(subTopic)

            subTopic = "%s%s%s%s" % (confSiteName, confSubTopicPrefix, boardNames[i], confCmdTopicSuffix)
            logger.debug("Subscribing to: %s", subTopic)                                 
            output_mid = client.subscribe(subTopic)
    
    def on_publish(client, userdata, mid):
        logger.debug("Published: %s", str(mid))

    def on_subscribe(client, userdata, mid, granted_qos):
        logger.debug("Subscribed: %s", str(mid))

    def on_message_output(client, userdata, msg):
        logger.debug("Output topic: %s", msg.topic)
        logger.debug("Output data: %s", msg.payload)
        #add to outputData list
        outputData.append(msg)

    def on_message(client, userdata, message):
        cmdQueue.put(message)

    def processCmdMessages():
        while not cmdQueue.empty():
            message = cmdQueue.get()
            if message is None:
                continue

            topic = message.topic
            payload = message.payload.decode("UTF-8")

            logger.debug("Message Received: %s %s", topic, payload)

            # Select board by name
            targetBoardName = topic.split("/")[2] # <sitename>/<subTopicPrefix>/<board_name>/

            targetBoardIndex = -1
            for i in range(len(boardNames)):
                if(boardNames[i] == targetBoardName):
                    targetBoardIndex = i

            logger.debug("Target board index is: %d", targetBoardIndex)
            if(targetBoardIndex >= 0):

                if(topic.split("/")[3] == confCmdTopicSuffix[1:]):
                    # Command to whole board
                    logger.debug("Targetting whole board %s", targetBoardName)
                    if(payload == confRelayOnCommandPayload):
                        boards[i].turnAllOn()
                    elif(payload == confRelayOffCommandPayload):
                        boards[i].turnAllOff()
                    elif(payload == confRelayStatusCommandPayload):
                        mqttc.publish(pubTopics[i], boards[i].readRelays(), qos=mqttQos,retain=mqttRetain)
                    else:
                        logger.warning("Unknown command: %s", payload)
                else:  
                    channelNumber = -1 
                    channelNumber = int(topic.split("/")[3][2:]) # <sitename>/<subTopicPrefix>/<board_name>/CH1/<cmdSuffix>

                    logger.debug("Targetting board %s CH%d", targetBoardName, channelNumber)

                    if(channelNumber>0 and channelNumber<9):
                        if(payload == confRelayOnCommandPayload):
                            logger.debug("Turning on CH%d on %s", channelNumber, targetBoardName)
                            boards[i].turnOnRelay(channelNumber)
                        elif(payload == confRelayOffCommandPayload):
                            logger.debug("Turning off CH%d on %s", channelNumber, targetBoardName)
                            boards[i].turnOffRelay(channelNumber)
                        else:
                            logger.warning("Unknown command: %s", payload)
                    else:
                        logger.warning("Incorrect channel number!, skipped")
            else:
                logger.warning("Target board not found, skipped")    
            
            updateStates()

    def updateStates():
        logger.debug("Updating relay states")
        for i in range(len(boardNames)):

            mqttc.publish(pubTopics[i], boards[i].readRelays(), qos=mqttQos,retain=mqttRetain)
            for j in range(8):
                mqttc.publish(pubTopics[i]+"/CH"+str(j+1)+confPubTopicStateSuffix, boards[i].getChannelState((j+1)), qos=mqttQos,retain=mqttRetain)
        logger.debug("Relay states updated")


    #called on exit
    #close serial, disconnect MQTT
    def cleanup():
        logger.info("Ending and cleaning up")
        modbusclient.close()
        mqttc.disconnect()

    def connectMqtt():
        try:
            logger.debug("Connecting to MQTT broker.")
            #attach MQTT callbacks
            mqttc.on_connect = on_connect
            mqttc.on_publish = on_publish
            mqttc.on_subscribe = on_subscribe
            mqttc.on_message = on_message
            mqttc.username_pw_set(credConfigParser.get('MQTT', 'mqttUsername'), credConfigParser.get('MQTT', 'mqttPasswd'))
            mqttc.message_callback_add(configParser.get('MQTT', 'callbackTopicPrefix') + confMqttClientName + configParser.get('MQTT', 'callbackTopicSuffix'), on_message_output)

            # Connect to broker. Try twice, as connect was failing when service started at boot
            try:
                mqttc.connect(configParser.get('MQTT', 'mqttServer'), configParser.getint('MQTT', 'mqttPort'), configParser.getint('MQTT', 'mqttTimeout'))
            except Exception:
                logger.exception("Exception during MQTT connect, sleep 10 seconds and retry", exc_info=True)
                time.sleep(10)
                mqttc.connect(configParser.get('MQTT', 'mqttServer'), configParser.getint('MQTT', 'mqttPort'), configParser.getint('MQTT', 'mqttTimeout'))

            # start the mqttc client thread
            mqttc.loop_start()
            
            logger.info("Modbus and MQTT clients started and connected!")
        except Exception:
            logger.exception("Exception during MQTT connect", exc_info=True)
            cleanup
            exit(1)

    def readRelays():
        logger.debug("Read Meter - not implemented yet :)")

    ############ MAIN PROGRAM START
    try:
        logger.info("Modbus to Mqtt service starting.")
        #connect to serial port
        connectval = modbusclient.connect()
        logger.debug("Modbus client connected.")
    except:
        logger.exception("Failed to connect modbus")
        #print "Failed to connect modbus"
        #unable to continue with no modbus connection
        raise SystemExit

    try:

        connectMqtt()
        # client.connect()

        # Publish initial states after connect
        updateStates()
            # Initial tests to toggle relays
            # logger.debug("Writing...")
            # boards[i].writeRelays([False,True,False,True,False,True,False,True])
            # mqttc.publish(pubTopics[i], boards[i].readRelays(), qos=mqttQos,retain=mqttRetain)
            # time.sleep(1)
            # logger.debug("Writing...")
            # boards[i].writeRelays([True,False,True,False,True,False,True,False])
            # mqttc.publish(pubTopics[i], boards[i].readRelays(), qos=mqttQos,retain=mqttRetain)

            # boards[i+1].setBaudRate9600N()
        
        # loop forever
        while(True):
            processCmdMessages()
            time.sleep(1)

        cleanup()
        logger.info('----------------- completed -----------------')

    # handle app closure
    except (KeyboardInterrupt):
        logger.exception("Interrupt received")
        #print "Interrupt received"
        cleanup()
    except (RuntimeError, SystemExit):
        logger.exception("uh-oh! time to die")
        #print "uh-oh! time to die"
        cleanup()
