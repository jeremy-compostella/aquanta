# aquanta

`aquanta` is an unofficial python library to communicate with the
Aquanta water heater smart controller. This library covers a limited
set of the device features.

```
>>> from aquanta import Aquanta
>>> aquanta = Aquanta('<YOUR-EMAIL>', '<YOUR-PASSWORD>')
```

Multiple aquanta devices can be attached to a single Aquanta
accounts. Similarly an `Aquanta` object list all these devices as
couples of identifier (`int`) and `AquantaDevice` object.

```
>>> list(aquanta)
[(19658, <aquanta.AquantaDevice object at 0x7f5c5037bd90>)]
```

The `AquantaDevice` object offers method to read the water heater
status and access its schedule. The schedule can be read and written
but the write feature has not been tested.

```
>>> aquanta[19658].water
{'temperature': 49.41, 'available': 1}
>>> aquanta[19658].infocenter
{'title': 'Aquanta', 'currentMode': {'type': 'timer'},
'records': [{'title': 'Controlling to Manual Setpoint',
             'type': 'setpoint', 'state': 'ongoing',
             'body': 'Aquanta is controlling to your specified setpoint'},
            {'title': 'Your Timer Is Running', 'type': 'timer', 
             'state': 'ongoing',
             'body': 'Aquanta is keeping your water heater off until 8:00AM tomorrow'}]}
>>> aquanta[19658].advanced
{'controlEnabled': True, 'intelEnabled': False, 'efficiencySelection': 0.5,
 'setPoint': 90, 'thermostatEnabled': True, 'touEnabled': False,
 'timerEnabled': True}
>>> aquanta[19658].timer
{'schedules': [{'start': {'hour': 8, 'minute': 15, 'second': 0},
                'end': {'hour': 14, 'minute': 30, 'second': 0},
                'daysOfWeek': [1, 2, 3, 4, 5], 'resolution': 2},
               {'start': {'hour': 8, 'minute': 15, 'second': 0},
                'end': {'hour': 14, 'minute': 30, 'second': 0},
                'daysOfWeek': [0, 6], 'resolution': 2}, 
               {'start': {'hour': 15, 'minute': 15, 'second': 0},
                'end': {'hour': 23, 'minute': 59, 'second': 59},
                'daysOfWeek': [1, 2, 3, 4, 5], 'resolution': 2},
               {'start': {'hour': 15, 'minute': 15, 'second': 0},
                'end': {'hour': 23, 'minute': 59, 'second': 59}, 
                'daysOfWeek': [0, 6], 'resolution': 2},
               {'start': {'hour': 0, 'minute': 0, 'second': 0},
                'end': {'hour': 8, 'minute': 0, 'second': 0},
                'daysOfWeek': [1, 2, 3, 4, 5], 'resolution': 2},
               {'start': {'hour': 0, 'minute': 0, 'second': 0},
                'end': {'hour': 8, 'minute': 0, 'second': 0},
                'daysOfWeek': [0, 6], 'resolution': 2}],
 'selectedResolution': 2}
```

The `AquantaDevice` object also provides methods to set the `boost` or
`away` mode time window. The `set_boost()` and `set_away()` method
parameters are two strings (`start` and `end`) of UTC time formatted
as `%Y-%m-%dT%H:%M:%S.000Z`.
