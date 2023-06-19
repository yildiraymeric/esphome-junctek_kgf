import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart, sensor
from esphome.const import (
    CONF_RAW,
    CONF_ID,
    CONF_ADDRESS,
    CONF_INPUT,
    CONF_NUMBER,
    CONF_HARDWARE_UART,
    CONF_TEMPERATURE,
    CONF_VOLTAGE,
    CONF_CURRENT,
    CONF_POWER,
    CONF_BATTERY_LEVEL,
    
    DEVICE_CLASS_VOLTAGE,
    STATE_CLASS_MEASUREMENT,
    UNIT_VOLT,
    UNIT_CELSIUS,
    UNIT_AMPERE,
    UNIT_WATT,
    UNIT_OHM,
    CONF_UPDATE_INTERVAL,
    UNIT_EMPTY,
    UNIT_PERCENT,
    ICON_EMPTY,
    ICON_THERMOMETER,
    ICON_FLASH,
    ICON_PERCENT,
    ICON_POWER,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_POWER,
)



DEPENDENCIES = ["uart"]

AUTO_LOAD = ["sensor"]

# sensors
CONF_CURRENT_DIRECTION="current_direction"
CONF_BATTERY_OHM="battery_ohm"

TYPES = [
    CONF_VOLTAGE,
    CONF_CURRENT,
    CONF_POWER,
    CONF_BATTERY_LEVEL,
    CONF_TEMPERATURE,
    CONF_CURRENT_DIRECTION,
    CONF_BATTERY_OHM
]

# variables
CONF_INVERT_CURRENT="invert_current"
CONF_SETTINGS_REFRESH="settings_refresh_seconds"
CONF_DATA_REFRESH="data_refresh_seconds"

JuncTekKGF = cg.global_ns.class_(
    "JuncTekKGF", cg.Component, uart.UARTDevice
)

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(JuncTekKGF),
            cv.Optional(CONF_ADDRESS, default=1): cv.int_range(1, 255),
            cv.Optional(CONF_VOLTAGE): sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT,
                icon=ICON_FLASH,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_VOLTAGE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_CURRENT): sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPERE,
                icon="mdi:current-dc",
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_CURRENT,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_POWER): sensor.sensor_schema(
                unit_of_measurement=UNIT_WATT,
                icon=ICON_POWER,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_BATTERY_LEVEL): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                icon=ICON_PERCENT,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_BATTERY,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_BATTERY_OHM): sensor.sensor_schema(
                unit_of_measurement=UNIT_OHM,
                icon="mdi:resistor",
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_BATTERY,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
             cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                icon=ICON_THERMOMETER,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_INVERT_CURRENT, default=False): cv.boolean, 
            cv.Optional(CONF_SETTINGS_REFRESH, default=30): cv.update_interval, 
            cv.Optional(CONF_DATA_REFRESH, default=10): cv.update_interval, 
            
            cv.Optional(CONF_CURRENT_DIRECTION, default=True): cv.boolean,
        }
    ).extend(uart.UART_DEVICE_SCHEMA)
    )

async def setup_conf(config, key, hub):
    if key in config:
        conf = config[key]
        sens = await sensor.new_sensor(conf)
        cg.add(getattr(hub, f"set_{key}_sensor")(sens))


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID], config[CONF_ADDRESS], config[CONF_INVERT_CURRENT], config[CONF_SETTINGS_REFRESH], config[CONF_DATA_REFRESH])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)
    for key in TYPES:
        await setup_conf(config, key, var)
