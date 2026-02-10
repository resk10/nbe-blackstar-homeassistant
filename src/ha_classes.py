import json
import re
import settings

def strip_invalid(text):
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)
    return re.sub(r"\s+", '_', text).lower()

class Resource:
    def __init__(self, component, type, resource):
        self.component = component
        self.type = type
        self.resource = resource

    def getHaTopic(self):
        return settings.config["ha_prefix"] + "/" + self.type + "/" + self.component.device.getUid() + "/" + self.component.getUid() + "/config"

    def getCommandTopic(self):
        return self.component.command_topic

    def getTempCommandTopic(self):
        return self.component.temperature_command_topic

    def getTempStateTopic(self):
        return self.component.temperature_state_topic

    def getStateTopic(self):
        return self.component.state_topic

class Device:
    def __init__(self, identifiers, name, sw_version, model, manufacturer):
        self.identifiers = identifiers
        self.name = name
        self.sw_version = sw_version
        self.model = model
        self.manufacturer = manufacturer

    def getName(self):
        return self.name

    def getUid(self):
        return strip_invalid(self.name)

    def getId(self):
        return self.identifiers

    def to_dict(self):
        # Home Assistant expects identifiers as a list
        return {
            "identifiers": [self.identifiers],
            "name": self.name,
            "sw_version": self.sw_version,
            "model": self.model,
            "manufacturer": self.manufacturer
        }

class Climate:
    def __init__(self, name, icon, current_temp_topic, max_temp, device):
        self.name = name
        self.temperature_unit = "C"
        self.current_temperature_topic = device.getUid() + "/" + current_temp_topic
        self.temperature_command_topic = device.getUid() + "/climate/" + strip_invalid(name) + "/command"
        self.temperature_state_topic = device.getUid() + "/climate/" + strip_invalid(name) + "/state"
        self.icon = icon
        self.max_temp = max_temp
        self.min_temp = 0
        self.modes = ["auto"]
        self.mode_state_topic = device.getUid() + "/bridge/static_auto_state"
        self.unique_id = strip_invalid(self.name) + "_" + device.getId()
        self.device = device
        self.availability_topic = device.getUid() + "/bridge/state"

    def getUid(self):
        return strip_invalid(self.name)

    def toJSON(self):
        payload = {
            "name": self.name,
            "temperature_unit": self.temperature_unit,
            "current_temperature_topic": self.current_temperature_topic,
            "temperature_command_topic": self.temperature_command_topic,
            "temperature_state_topic": self.temperature_state_topic,
            "max_temp": self.max_temp,
            "min_temp": self.min_temp,
            "modes": self.modes,
            "mode_state_topic": self.mode_state_topic,
            "unique_id": self.unique_id,
            "availability_topic": self.availability_topic,
            "device": self.device.to_dict()
        }
        if self.icon != "none":
            payload["icon"] = self.icon
        return json.json.dumps(payload, indent=5)

class Switch:
    def __init__(self, icon, name, device):
        self.icon = icon
        self.name = name
        self.state_topic = device.getUid() + "/switch/" + strip_invalid(name) + "/state"
        self.command_topic = device.getUid() + "/switch/" + strip_invalid(name) + "/command"
        self.availability_topic = device.getUid() + "/bridge/state"
        self.unique_id = strip_invalid(self.name) + "_" + device.getId()
        self.device = device
        self.payload_on = "ON"
        self.payload_off = "OFF"

    def getUid(self):
        return strip_invalid(self.name)

    def toJSON(self):
        payload = {
            "name": self.name,
            "state_topic": self.state_topic,
            "command_topic": self.command_topic,
            "availability_topic": self.availability_topic,
            "unique_id": self.unique_id,
            "payload_on": self.payload_on,
            "payload_off": self.payload_off,
            "device": self.device.to_dict()
        }
        if self.icon != "none":
            payload["icon"] = self.icon
        return json.dumps(payload, indent=7)

class Sensor:
    def __init__(self, icon, device_class, unit_of_measurement, state_class, name, device):
        self.icon = icon
        self.device_class = device_class
        self.unit_of_measurement = unit_of_measurement
        self.state_class = state_class
        self.name = name
        self.state_topic = device.getUid() + "/sensor/" + strip_invalid(name) + "/state"
        self.availability_topic = device.getUid() + "/bridge/state"
        self.unique_id = strip_invalid(self.name) + "_" + device.getId()
        self.device = device

    def getUid(self):
        return strip_invalid(self.name)

    def toJSON(self):
        payload = {
            "name": self.name,
            "state_topic": self.state_topic,
            "availability_topic": self.availability_topic,
            "unique_id": self.unique_id,
            "device": self.device.to_dict()
        }
        if self.icon != "none":
            payload["icon"] = self.icon
        if self.device_class != "none":
            payload["device_class"] = self.device_class
        if self.unit_of_measurement != "none":
            payload["unit_of_measurement"] = self.unit_of_measurement
        if self.state_class != "none":
            payload["state_class"] = self.state_class

        return json.dumps(payload, indent=8)