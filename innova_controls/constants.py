from innova_controls.mode import Mode

CMD_POWER_ON = "power/on"
CMD_POWER_OFF = "power/off"
CMD_NIGHT_MODE = "set/feature/night"
CMD_SET_TEMP = "set/setpoint"
CMD_ROTATION = "set/feature/rotation"
CMD_FAN_SPEED = "set/fan"
CMD_STATUS = "status"

ROTATION_ON = 0
ROTATION_OFF = 7

NIGHT_MODE_ON = 1
NIGHT_MODE_OFF = 0

MIN_TEMP = 16
MAX_TEMP = 31

CONNECTION_TIMEOUT = 20

UNKNOWN_MODE = Mode("", -1)
