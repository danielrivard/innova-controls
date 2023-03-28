[![PyPI version](https://badge.fury.io/py/innova-controls.svg)](https://badge.fury.io/py/innova-controls)

# Innova Control API

Tested on a [Innova 2.0 unit](https://www.innovaenergie.com/en/products/air-conditioning-without-outdoor-unit/2.0-verticale/2.0/)

Also supports [AirLeaf](https://www.innovaenergie.com/en/products/fancoils/airleaf/)

## Installation
``` pip install innova_controls```

## Innova class usage
See [test_main.py](test_main.py) for some example usage. 

This is far from perfect documentation, but it is a start.

## Communication protocol

### Local Mode

All commands are sent to the unit itself through http at its network IP address: **http://[IP_ADDRESS]/api/v/1**.

### Cloud Mode

Commands are sent to Innova's cloud services at **https://innovaenergie.cloud/api/v/1** (or **https://fancoil.innovaenergie.cloud/api/v/1** for AirLeaf, but currently not working). The serial number and the MAC Address of the unit are needed when using cloud mode.

The following custom http headers are added to requests to identify units
  * "X-serial": UNIT_SERIAL_NUMBER
  * "X-UID": UNIT_MAC_ADDRESS

### Protocol definition

We just need to append the following commands and parameters where needed.

Ex: ```curl http://192.168.1.155/api/v/1/status```

It is highly recommended to set the IP of your unit to a static DHCP address.

#### 2.0 Commands and Statuses
|Action|HTTP Verb|API Endpoint|Data Needed (`Content-Type: application/x-www-form-urlencoded`)|Extra Info|
|---|---|---|---|---|
|Status|GET|/status||Returns json object|
|Power ON|POST|/power/on|||
|Power OFF|POST|/power/off|||
|Scheduling ON|POST|/set/calendar/on|||
|Scheduling OFF (Manual)|POST|/set/calendar/off|||
|Night Mode ON|POST|/set/feature/night|value=1||
|Night Mode OFF|POST|/set/feature/night|value=0||
|Set point|POST|/set/setpoint|p_temp=24||
|Rotation ON|POST|/set/feature/rotation|value=0||
|Rotation OFF|POST|/set/feature/rotation|value=7||
|Fan Speed|POST|/set/fan|value=[0-4]|0=auto,1=low,2=med,3=high,4=high++|
|Cooling|POST|/set/mode/cooling|||
|Heating|POST|/set/mode/heating|||
|Dehumidification|POST|/set/mode/dehumidification|||
|Fan Only|POST|/set/mode/fanonly|||
|Auto|POST|/set/mode/auto|||


JSON returned by status endpoint:
```json
{
    "RESULT": {
        "a": [],
        "cci": 0,
        "ccv": 0,
        "cfg_lastWorkingMode": 4,
        "cloudConfig": 1,
        "cloudStatus": 4,
        "cm": 0,                       <--- Scheduling Mode: 0=off, 1=on
        "connectionStatus": 2,
        "coolingDisabled": 0,
        "cp": 0,
        "daynumber": 0,
        "fr": 7,                       <--- Fan Rotation: 0=on, 7=off
        "fs": 0,                       <--- Fan Speed: 0=auto, 1=low, 2=med, 3=high, 4=high++
        "heap": 11760,
        "heatingDisabled": 1,
        "heatingResistance": 0,
        "hotelMode": 0,
        "inputFlags": 0,
        "kl": 0,
        "lastRefresh": 3956,
        "ncc": 0,
        "nm": 0,                        <--- Night Mode: 0=off, 1=on
        "ns": 0,
        "ps": 0,                        <--- Power: 0=off, 1=on
        "pwd": "************",
        "sp": 26,                       <--- Temperature Set point
        "t": 16,                        <--- Ambient Temperature
        "timerStatus": 0,
        "uptime": 159660,
        "uscm": 0,
        "wm": 4                         <--- Working Mode: 0=heating, 1=cooling, 3=dehumidification, 4=fanonly. 5=auto
    },
    "UID": "[MAC ADDRESS]",
    "deviceType": "001",
    "net": {
        "dhcp": "1",
        "gw": "XXX.XXX.XXX.XXX",
        "ip": "XXX.XXX.XXX.XXX",
        "sub": "255.255.255.0"
    },
    "setup": {
        "name": "Device Name",
        "serial": "YYYYYYYYY"
    },
    "success": true,
    "sw": {
        "V": "1.0.42"
    },
    "time": {
        "d": 5,
        "h": 17,
        "i": 40,
        "m": 2,
        "y": 2022
    }
}

```

#### AirLeaf Commands and Statuses
|Action|HTTP Verb|API Endpoint|Data Needed (`Content-Type: application/json`)|Extra Info|
|---|---|---|---|---|
|Status|GET|/status||Returns json object|
|Power ON|POST|/power/on|||
|Power OFF|POST|/power/off|||
|Scheduling ON|POST|/set/calendar/on|||
|Scheduling OFF (Manual)|POST|/set/calendar/off|||
|Set point|POST|/set/setpoint|temp=240|On AirLeaf, temperatures are multiplied by 10|
|Fan Function Auto|POST|/set/function/auto|value=1||
|Fan Function Night|POST|/set/function/night|value=1||
|Fan Function Min|POST|/set/function/min|value=1||
|Fan Function Max|POST|/set/function/max|value=1||
|Cooling|POST|/set/mode/cooling|||
|Heating|POST|/set/mode/heating|||


JSON returned by status endpoint:
```json
{
  "success": true,
  "sw": {
    "V": "1.0.3"
  },
  "UID": "f4:cf:a2:5f:29:ef",
  "deviceType": "002",
  "time": {
    "d": 18,
    "m": 10,
    "y": 2022,
    "h": 6,
    "i": 14
  },
  "net": {
    "gw": "XXX.XXX.XXX.XXX",
    "ip": "XXX.XXX.XXX.XXX",
    "sub": "255.255.255.0"
    "dhcp": "1"
  },
  "setup": {
    "name": "Device Name",
    "serial": "YYYYYYYYY"
  },
  "RESULT": {
    "sp": 200,                        <--- Temperature Set point (x10)
    "wm": 3,                          <--- Working Mode: 3=heating. 5=cooling
    "fn": 1,                          <--- Fan Function: 1=auto, 2=night, 3=min, 4=max
    "kl": 0,
    "lastworkingModeSet": 0,
    "ps": 0,                          <--- Power: 0=off, 1=on
    "cm": 0,                          <--- Scheduling Mode: 0=off, 1=on
    "a": [],
    "ta": 210,                        <--- Ambient Temperature (x10)
    "tw": 219,                        <--- Water Temperature (x10)
    "ns": 0,
    "cloudStatus": 4,
    "connectionStatus": 2,
    "cloudConfig": 1,
    "timerStatus": 0,
    "inputFlags": 0,
    "ncc": 0,
    "lcc": 0,
    "pwd": "",
    "heap": 11496,
    "ccv": 0,
    "cci": 0,
    "daynumber": 0,
    "uptime": 90675,
    "fclFw": 24,
    "uscm": 0,
    "lastRefresh": 2
  }
}

```
