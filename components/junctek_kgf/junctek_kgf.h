#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/uart/uart.h"

using namespace esphome;

class JuncTekKGF
  : public esphome::Component
  , public uart::UARTDevice
{
public:
  JuncTekKGF(unsigned address = 1, bool invert_current = false, unsigned settings_refresh_seconds_ = 30, unsigned data_refresh_seconds_ = 10);

  void set_address(unsigned address) { address_ = address; }
  void set_invert_current(bool invert_current) { invert_current_ = invert_current; }
  void set_settings_refresh_seconds(unsigned settings_refresh_seconds) { settings_refresh_seconds_ = settings_refresh_seconds * 1000; }
  void set_data_refresh_seconds(unsigned data_refresh_seconds) { data_refresh_seconds_ = data_refresh_seconds * 1000; }

  void set_voltage_sensor(sensor::Sensor *voltage_sensor) { voltage_sensor_ = voltage_sensor; }
  void set_current_sensor(sensor::Sensor *current_sensor) { current_sensor_ = current_sensor; }
  void set_power_sensor(sensor::Sensor *power_sensor) { power_sensor_ = power_sensor; }
  void set_current_direction_sensor(sensor::Sensor *current_direction_sensor) { current_direction_sensor_ = current_direction_sensor; }

  void set_battery_ohm_sensor(sensor::Sensor *battery_ohm_sensor) { battery_ohm_sensor_ = battery_ohm_sensor; }
  void set_battery_level_sensor(sensor::Sensor *battery_level_sensor) { battery_level_sensor_ = battery_level_sensor; }
  void set_battery_life_sensor(sensor::Sensor *battery_life_sensor) { battery_life_sensor_ = battery_life_sensor; }
  void set_amp_hour_remain_sensor(sensor::Sensor *amp_hour_remain_sensor) { amp_hour_remain_sensor_ = amp_hour_remain_sensor; }
  void set_watt_hour_remain_sensor(sensor::Sensor *watt_hour_remain_sensor) { watt_hour_remain_sensor_ = watt_hour_remain_sensor; }
  void set_amp_hour_total_sensor(sensor::Sensor *amp_hour_total_sensor) { amp_hour_total_sensor_ = amp_hour_total_sensor; }

  void set_relay_status_sensor(sensor::Sensor *relay_status_sensor) { relay_status_sensor_ = relay_status_sensor; }
  void set_temperature_sensor(sensor::Sensor *temperature) { temperature_ = temperature; }

  void set_runtime_sensor(sensor::Sensor *runtime_sensor) { runtime_sensor_ = runtime_sensor; }
  
  void dump_config() override;
  void loop() override;

  float get_setup_priority() const;// override;

protected:
  bool readline();
  void handle_line();
  void handle_status(const char* buffer);
  void handle_settings(const char* buffer);
  void request_data(uint8_t data_id);
  void decode_data(std::vector<uint8_t> data);
  bool verify_checksum(int checksum, const char* buffer);

  // const unsigned address_;
  unsigned address_;
  bool invert_current_;
  unsigned settings_refresh_seconds_;
  unsigned data_refresh_seconds_;

  sensor::Sensor* voltage_sensor_{nullptr};
  sensor::Sensor* current_sensor_{nullptr};
  sensor::Sensor* power_sensor_{nullptr};
  sensor::Sensor* current_direction_sensor_{nullptr};

  sensor::Sensor* battery_ohm_sensor_{nullptr};
  sensor::Sensor* battery_level_sensor_{nullptr};
  sensor::Sensor* battery_life_sensor_{nullptr};
  sensor::Sensor* amp_hour_remain_sensor_{nullptr};
  sensor::Sensor* watt_hour_remain_sensor_{nullptr};
  sensor::Sensor* amp_hour_total_sensor_{nullptr};

  sensor::Sensor* relay_status_sensor_{nullptr};
  sensor::Sensor* temperature_{nullptr};
  
  sensor::Sensor* runtime_sensor_{nullptr};

  static constexpr int MAX_LINE_LEN = 120;
  std::array<char, MAX_LINE_LEN> line_buffer_;
  size_t line_pos_ = 0;

  optional<float> battery_capacity_;
  optional<unsigned long> last_settings_;
  optional<unsigned long> last_stats_;

};
