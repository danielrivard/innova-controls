from flask import Flask, jsonify, request

app = Flask(__name__)

deviceType = "001"
mac_address = "06:1A:02:0A:E4:8D"
serial = "IN2014752"

water_temp = 215
target_temp = 20
ambient_temp = 21
if deviceType == "002":
    target_temp = target_temp * 10
    ambient_temp = ambient_temp * 10


def success_response(success=True):
    return jsonify({"success": success})


@app.route("/api/v/1/power/on", methods=["POST"])
def power_on():
    return success_response()


@app.route("/api/v/1/power/off", methods=["POST"])
def power_off():
    return success_response()


@app.route("/api/v/1/set/feature/night", methods=["POST"])
def night_mode():
    return success_response()


@app.route("/api/v/1/set/setpoint", methods=["POST"])
def set_point():
    print(request.content_type)
    if request.content_type == "application/x-www-form-urlencoded":
        print(request.form.to_dict())
    if request.content_type == "application/json":
        print(request.json)
    return success_response()


@app.route("/api/v/1/set/feature/rotation", methods=["POST"])
def rotation():
    return success_response()


@app.route("/api/v/1/set/fan", methods=["POST"])
def fan_rotation():
    print(request.content_type)
    print(request.form.to_dict())
    return success_response()


@app.route("/api/v/1/set/mode/cooling", methods=["POST"])
def cooling():
    return success_response()


@app.route("/api/v/1/set/mode/heating", methods=["POST"])
def heat():
    return success_response()


@app.route("/api/v/1/set/mode/dehumidification", methods=["POST"])
def dehumidification():
    return success_response()


@app.route("/api/v/1/set/mode/fanonly", methods=["POST"])
def fanonly():
    return success_response()


@app.route("/api/v/1/set/mode/auto", methods=["POST"])
def auto():
    return success_response()


@app.route("/api/v/1/set/function/auto", methods=["POST"])
def function_auto():
    return success_response()


@app.route("/api/v/1/set/function/night", methods=["POST"])
def function_night():
    return success_response()


@app.route("/api/v/1/set/function/min", methods=["POST"])
def function_min():
    return success_response()


@app.route("/api/v/1/set/function/max", methods=["POST"])
def function_max():
    return success_response()


@app.route("/api/v/1/status", methods=["GET"])
def status():
    status = {
        "RESULT": {
            "a": [],
            "cci": 0,
            "ccv": 0,
            "cfg_lastWorkingMode": 0,
            "cloudConfig": 1,
            "cloudStatus": 4,
            "cm": 0,
            "connectionStatus": 2,
            "coolingDisabled": 0,
            "cp": 0,
            "daynumber": 0,
            "fr": 0,
            "fs": 0,
            "fn": 1,
            "heap": 11632,
            "heatingDisabled": 0,
            "heatingResistance": 0,
            "hotelMode": 0,
            "inputFlags": 0,
            "kl": 0,
            "lastRefresh": 2,
            "ncc": 0,
            "nm": 0,
            "ns": 0,
            "ps": 1,
            "pwd": "",
            "sp": target_temp,
            "t": ambient_temp,
            "ta": ambient_temp,
            "tw": water_temp,
            "timerStatus": 0,
            "uptime": 112920,
            "uscm": 0,
            "wm": 3,
        },
        "UID": mac_address,
        "deviceType": deviceType,
        "net": {
            "dhcp": "1",
            "gw": "192.168.1.1",
            "ip": "192.168.1.223",
            "sub": "255.255.255.0",
        },
        "setup": {"name": "InnovaSim", "serial": serial},
        "success": True,
        "sw": {"V": "1.0.42"},
        "time": {"d": 1, "h": 18, "i": 45, "m": 2, "y": 2023},
    }
    return jsonify(status)


print(__name__)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
