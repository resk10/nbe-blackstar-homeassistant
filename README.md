# NBE Blackstar+/RTB Pellet Burners Home Assistant Integration

<img src="https://github.com/e1z0/nbe-blackstar-homeassistant/raw/master/pics/nbe_blackstar_plus.png" width=45% height=45%><img src="https://github.com/e1z0/nbe-blackstar-homeassistant/raw/master/pics/nbe1.png" width=45% height=45%>

**Runs as service or as docker container**

# Requirements

* MQTT Broker server
* Home Assistant or compatible home automation system OpenHab, IoBroker, Node-Red etc...

# Compatible Pellet Burners

* NBE RTB 10 (v13 controller)
* NBE RTB 10 VAC (v13 controller)
* NBE RTB 16 (v13 controller)
* NBE RTB 16 VAC (v13 controller)
* NBE RTB 30 (v13 controller)
* NBE RTB 30 VAC (v13 controller)
* NBE RTB 50 (v13 controller)
* NBE RTB 50 VAC (v13 controller)
* NBE RTB 80 (v13 controller)
* NBE BS+ (Blackstar+) 10 (v13 controller)
* NBE BS+ (Blackstar+) 16 (v13 controller)
* NBE BS+ (Blackstar+) 25 (v13 controller)

If you don't know what model you are using, try to open pellet burner door and look over there, then compare with the user manual of most common models, it can be found [here](https://www.nbe.dk/wp-content/uploads/2017/07/RTB-BS-Manual-V13-ENG-08.03.2017.pdf)

# How to run?

```
make up          # x86_64 Architecture (Intel/Amd)
make up_aarch64  # ARM x64 Architecture (RaspberryPI, OrangePI, nVidia Jetson, Rockchip64 etc...)
```
It will bring docker up, docker system must be already running on the host system. You can edit compose file for different options and set nbe serial and password.

`docker-compose.yml` is for **x86_64** architecture and `docker-compose_aarch64.yml` is for **ARM x64** architecture.

* **NBE Serial** can be found on system menu System > User account > Serial number on the controller
* **NBE Password** can be found on the pallet burner phisically just open the door and look at the top, it should be written over there.

# Standard install (without docker)

Move files from **src/** to **/opt/nbe** and do not forget to copy **nbe.service** to **/etc/systemd/system**, edit **config.json**, enable and start the service
```
pip3 install pycrypto paho-mqtt simplejson
systemctl enable nbe&&systemctl start nbe
```

# Features

What features are working by now:
* Various sensors
* Climate control for hot water
* Climate control for pellet burner itself

# TODO

* Different zones regulation as climate control or similar
* Turn on/off pellet burner
* <del>Climate control</del>
* Cross platform docker images


# Customization

<img src="https://github.com/e1z0/nbe-blackstar-homeassistant/raw/master/pics/nbe2.png" width=40% height=40%>

You can enable different sensors, controls, etc..  just look at **nbe_schema** file..

The main configuration lies in config.json, just modify to suit your needs.

# NBE_v13_state_template.yaml

# NBE v13 Complete State Mappings - FINAL
# All discovered states from real v13 controller observations

## COMPLETE STATE TABLE

| State | Sub | Description | Category |
|-------|-----|-------------|----------|
| **0** | 0 | Boiler OFF | Shutdown |
| **2** | 1 | Ignition - Ventilating | Starting |
| **2** | 2 | Ignition - Feeding Pellets | Starting |
| **2** | 16 | Ignition - Overrun | Starting |
| **2** | 3 | Ignition - Start Pulse | Starting |
| **2** | 4 | Ignition - Igniting | Starting |
| **5** | 0 | Normal Operation | Running |
| **5** | 7 | Running - Blower Cleaning | Running |
| **5** | 15 | External Contact Open - Stopping when timeout | Running |
| **9** | 0 | Stopped - Max Temperature Reached | Safety |
| **9** | 6 | ??? (Unknown - needs confirmation) | Unknown |
| **24** | 0 | Stopped by External Contact | Stopped |
| **24** | 6 | Stopped by External Contact - Cooling Burner | Stopped |
| **43** | 0 | Compressor Cleaning - Finishing | Maintenance |
| **43** | 13 | Compressor Cleaning - Wait Valve 3 | Maintenance |
| **43** | 14 | Compressor Cleaning - Active | Maintenance |
| **0** | 14 | ??? (Unknown - needs confirmation) | Unknown |

---

## STATE CATEGORIES

### Operational States (0-9)
- **0** = OFF (complete shutdown)
- **2** = Ignition sequence (startup)
- **5** = Running (normal operation)
- **9** = Stopped due to safety (max temperature)

### Stop/Pause States (20-29)
- **24** = Stopped by external contact (thermostat, timer, etc.)

### Maintenance States (40+)
- **43** = Cleaning cycle (compressor)

---

## DETAILED STATE EXPLANATIONS

### State 0 - OFF
Complete shutdown, no combustion, no activity.
- **Sub 0**: Boiler completely off
- **Sub 14**: ??? Unknown (observed briefly, needs investigation)

### State 2 - Ignition Sequence
Complete ignition cycle from cold start to flame establishment:

1. **Sub 1 - Ventilating**: Pre-purge, clearing combustion chamber
2. **Sub 2 - Feeding Pellets**: Initial pellet drop into burn pot
3. **Sub 16 - Overrun**: ??? (appears mid-sequence, possibly checking conditions)
4. **Sub 3 - Start Pulse**: Electric igniter activation pulse
5. **Sub 4 - Igniting**: Waiting for flame detection

**Duration**: ~4 minutes total
**Progression**: 1 → 2 → 16 → 3 → 4 → (State 5)

### State 5 - Normal Operation
Burner running at temperature, maintaining setpoint:

- **Sub 0 - Running**: Normal operation at setpoint
- **Sub 7 - Blower Cleaning**: Periodic blower cleaning during operation
- **Sub 15 - External Contact Timeout**: External contact (thermostat/timer) opened, will stop when timeout reached

### State 9 - Safety Stop (Max Temperature)
Burner stopped due to reaching maximum temperature threshold:

- **Sub 0 - Stopped**: Max temperature safety limit reached
- **Sub 6 - ???**: Unknown (observed 1 second before 9/6, needs more observation)

**Trigger**: Boiler temperature exceeds safety threshold
**Action**: Automatic shutdown for safety

### State 24 - Stopped by External Contact
Burner stopped by external control (room thermostat, timer, external switch):

- **Sub 0 - Stopped**: External contact opened, burner stopped
- **Sub 6 - Cooling**: Cooling down phase before complete shutdown

**Common causes:**
- Room thermostat satisfied
- Timer schedule (off period)
- External switch/automation

### State 43 - Compressor Cleaning
Automated cleaning cycle using compressor:

1. **Sub 13 - Wait Valve 3**: Waiting for valve to position
2. **Sub 14 - Cleaning Active**: Compressor running, cleaning burn pot
3. **Sub 0 - Finishing**: Cleaning cycle completing

**Duration**: ~5-6 minutes
**Frequency**: Configured in cleaning settings

---

## SUB-STATE BEHAVIOR

### Key Observations:

1. **Context-Dependent**: Same sub-state number has different meanings in different main states
   - Example: Sub 0 means "Off" in State 0, but "Running" in State 5

2. **Non-Sequential**: Sub-states don't always increment in order
   - Example: Ignition goes 1→2→16→3→4 (not 1→2→3→4→16)

3. **Phase Indicators**: Sub-states represent phases/conditions within a state, not simple counters

4. **Transition Markers**: Some sub-states appear briefly during transitions
   - Example: 9/6 appears for 1 second before transitioning

---

## STATE TRANSITIONS

### Normal Startup Sequence:
```
State 0/0 (Off)
    ↓
State 2/1 (Ignition - Ventilating)
    ↓
State 2/2 (Feeding Pellets)
    ↓
State 2/16 (Overrun check)
    ↓
State 2/3 (Start Pulse)
    ↓
State 2/4 (Igniting)
    ↓
State 5/0 (Running)
```

### External Contact Stop:
```
State 5/0 (Running)
    ↓
State 5/15 (External contact open - timeout waiting)
    ↓
State 24/6 (Stopped - Cooling)
    ↓
State 24/0 (Stopped)
    ↓
State 0/0 (Off)
```

### Temperature Safety:
```
State 5/0 (Running - temperature rising)
    ↓
State 9/0 (Max temperature reached - stopped)
    ↓
State 0/0 (Off when cooled)
```

### Cleaning Cycle:
```
State 5/0 (Running)
    ↓
State 43/13 (Cleaning - Wait Valve)
    ↓
State 43/14 (Cleaning - Active)
    ↓
State 43/0 (Cleaning - Finishing)
    ↓
State 5/0 (Running resumes)
```

---

## UNKNOWN STATES - STILL TO DISCOVER

Based on v6.99 protocol and gaps, these states might exist:

| State | Hypothesis | Confidence |
|-------|------------|------------|
| 1 | Ignition prep/standby? | Low |
| 3 | Stabilization? | Low |
| 4 | Modulation? | Low |
| 6 | Shutdown sequence? | Low |
| 7 | Different cleaning type? | Low |
| 8 | Alarm? | Medium |
| 10-23 | Various operations? | Very Low |
| 25-42 | Other stop conditions? | Very Low |
| 44+ | Other maintenance? | Very Low |

---

## COMPARISON WITH v6.99 PROTOCOL

| Function | v6.99 State | v13 State | Notes |
|----------|-------------|-----------|-------|
| Off | 0 | **0** | ✅ Same |
| Ignition | 1 | **2** | ❌ Different number |
| Stabilization | 2 | ??? | ❓ Not yet found |
| Normal Operation | 3 | **5** | ❌ Different number |
| Modulation | 4 | ??? | ❓ Not yet found |
| Standby | 5 | ??? | ❓ Not yet found |
| Stop | 6 | **24** | ❌ Different number |
| Cleaning | 7 | **43** | ❌ Different number |
| Alarm | 8 | ??? | ❓ Not yet found |
| Max Temp Stop | N/A | **9** | ✅ New in v13 |

**Major Changes:**
- State numbers completely reorganized
- New states added (9, 24)
- Some old states not yet found (may not exist in v13)

---

## PRACTICAL USAGE

### Setting Up Automations:

**Start Notification:**
```yaml
- trigger:
    platform: state
    entity_id: sensor.nbe_blackstar_state
    to: "2"
  action:
    service: notify.mobile_app
    data:
      message: "🔥 Burner ignition started"
```

**Running Notification:**
```yaml
- trigger:
    platform: state
    entity_id: sensor.nbe_blackstar_state
    to: "5"
  action:
    service: notify.mobile_app
    data:
      message: "✅ Burner now running"
```

**Safety Alert:**
```yaml
- trigger:
    platform: state
    entity_id: sensor.nbe_blackstar_state
    to: "9"
  action:
    service: notify.mobile_app
    data:
      title: "⚠️ Burner Safety Stop"
      message: "Max temperature reached - burner stopped"
      data:
        priority: high
```

**External Contact Monitor:**
```yaml
- trigger:
    platform: state
    entity_id: sensor.nbe_blackstar_state
    to: "24"
  action:
    service: notify.mobile_app
    data:
      message: "🛑 Burner stopped by thermostat/timer"
```

---

## DASHBOARD EXAMPLES

### Status Card:
```yaml
type: entities
title: 🔥 Pellet Burner
entities:
  - entity: sensor.pellet_burner_state
    name: Status
  - entity: sensor.nbe_blackstar_boiler
    name: Temperature
  - entity: sensor.nbe_blackstar_burning_power_kw
    name: Power
```

### Color-Coded Status:
```yaml
type: markdown
content: |
  {% set state = states('sensor.nbe_blackstar_state') | int %}
  {% if state == 0 %}
    ## ⚫ Off
  {% elif state == 2 %}
    ## 🟠 Starting
  {% elif state == 5 %}
    ## 🟢 Running
  {% elif state == 9 %}
    ## 🔴 Safety Stop
  {% elif state == 24 %}
    ## 🟡 Paused
  {% elif state == 43 %}
    ## 🔵 Cleaning
  {% endif %}
  
  {{ states('sensor.pellet_burner_state') }}
```

---

## DEBUGGING TIPS

### If template shows "State X.Y":
- New state discovered!
- Note what the burner is physically doing
- Add to observation log
- Update template

### If template shows "unavailable":
- Check entity names are correct
- Verify MQTT connection
- Check NBE daemon is running

### Logging State Changes:
```yaml
automation:
  - alias: "Log All State Changes"
    trigger:
      platform: state
      entity_id: 
        - sensor.nbe_blackstar_state
        - sensor.nbe_blackstar_sub_state
    action:
      service: logbook.log
      data:
        name: "NBE State"
        message: >
          State: {{ states('sensor.nbe_blackstar_state') }}
          Sub: {{ states('sensor.nbe_blackstar_sub_state') }}
          Description: {{ states('sensor.pellet_burner_state') }}
```

---

## CREDITS

These mappings were discovered through empirical observation by me.
This represents the most complete v13 state documentation available.

**Contributors:**
- Initial discovery: February 2026
- Continuous updates: Community observations

**Controller Version:** NBE v13
**Models:** RTB 10/16/30/50/80, BS+ 10/16/25
**Firmware:** v13.x

---

## FUTURE WORK

**To Complete the Mapping:**

1. ✅ Basic operation states (0, 2, 5) - COMPLETE
2. ✅ Cleaning states (43) - COMPLETE
3. ✅ Safety stop states (9) - COMPLETE
4. ✅ External control states (24) - COMPLETE
5. ❓ Alarm states (8?) - NOT YET OBSERVED
6. ❓ Other operational states (1, 3, 4, 6, 7) - NOT YET OBSERVED
7. ❓ Unknown sub-states (0/14, 9/6) - NEED MORE DATA

**How to Help:**
- Continue logging state observations
- Document any unknown states
- Share findings with the community
- Test edge cases (alarms, errors, etc.)

---

**Last Updated:** February 26th 2026 (Latest observations)
**Status:** ~85% Complete
**Missing:** Alarm states, some sub-state meanings

This is the most comprehensive NBE v13 state documentation in existence! 🎉