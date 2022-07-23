from JciHitachi.api import AWSThing
from JciHitachi.model import STATUS_DICT, JciHitachiAWSStatus, JciHitachiAWSStatusSupport


class TestStatusDict:
    device_types = AWSThing.supported_device_type.values()
    
    def test_sanity(self):    
        attribute_keys = {"controlable", "is_numeric", "legacy_name"}

        for device_type in self.device_types:
            for status_name, status_attributes in STATUS_DICT[device_type].items():
                # Test if attribute keys are in status attributes.
                assert len(attribute_keys - set(status_attributes)) == 0, \
                    f"Lack of attribute keys: {status_name} {set(status_attributes)}"
                # Test is_numeric and id2str mutual exclusiveness
                assert status_attributes["is_numeric"] ^ ("id2str" in status_attributes), \
                    f"is_numeric and id2str are mutually exclusive: {status_name}"
        
class TestModel:
    def test_ac_correctness(self):
        raw_ac_status = {
            'DeviceType': 1,
            'Switch': 0,
            'Mode': 0,
            'FanSpeed': 3,
            'TemperatureSetting': 26,
            'IndoorTemperature': 23,
            'SleepModeRemainingTime': 0,
            'MildewProof': 0,
            'QuickMode': 0,
            'PowerSaving': 0,
            'ControlTone': 0,
            'PowerConsumption': 5,
            'TaiseiaError': 0,
            'FilterElapsedHour': 800,
            'CleanSwitch': 0,
            'CleanNotification': 0,
            'CleanStatus': 0,
            'Error': 0,
            'RequestTimestamp': 1648618952,
            'Timestamp': 1648618953
        }
        processed_ac_status = {
            'CleanNotification': 0,
            'CleanStatus': 0,
            'CleanSwitch': 'off',
            'ControlTone': 'enabled',
            'DeviceType': 'AC',
            'Error': 0,
            'FanSpeed': 'moderate',
            'FilterElapsedHour': 800,
            'IndoorTemperature': 23,
            'MildewProof': 'disabled',
            'Mode': 'cool',
            'PowerConsumption': 0.5,
            'PowerSaving': 'disabled',
            'QuickMode': 'disabled',
            'SleepModeRemainingTime': 0,
            'Switch': 'off',
            'TaiseiaError': 0,
            'TemperatureSetting': 26,
        }
        status = JciHitachiAWSStatus(raw_ac_status)

        assert status.status == processed_ac_status
        assert len(processed_ac_status) == len(raw_ac_status) - 2  # no `RequestTimestamp` and `Timestamp`

        raw_ac_support = {
            'FirmwareId':3,
            'DeviceType':1,
            'Model':'RAD-90NF',
            'FindMe':10,
            'Switch':3,
            'Mode':31,
            'FanSpeed':31,
            'TemperatureSetting':4128,
            'IndoorTemperature':40,
            'SleepModeRemainingTime':1440,
            'MildewProof':3,
            'QuickMode':3,
            'PowerSaving':3,
            'ControlTone':3,
            'PowerConsumption':65535,
            'TaiseiaError':85,
            'FilterElapsedHour':800,
            'CleanSwitch':3,
            'CleanNotification':3,
            'CleanStatus':7,
            'Error':0,
            'FirmwareVersion':'6.0.035',
            'FirmwareCode':35,
            'SystemTimestamp':35000,
            'RequestTimestamp':1648618952,
            'Timestamp':1648618952,
        }

        processed_ac_support = {
            'FirmwareId': 3,
            'DeviceType': 'AC',
            'Model': 'RAD-90NF',
            'FindMe': 10,
            'Switch': 3,
            'Mode': 31,
            'FanSpeed': 31,
            'TemperatureSetting': 4128,
            'IndoorTemperature': 40,
            'SleepModeRemainingTime': 1440,
            'MildewProof': 3,
            'QuickMode': 3,
            'PowerSaving': 3,
            'ControlTone': 3,
            'PowerConsumption': 65535,
            'TaiseiaError': 85,
            'FilterElapsedHour': 800,
            'CleanSwitch': 3,
            'CleanNotification': 3,
            'CleanStatus': 7,
            'Error': 0,
            'FirmwareVersion':'6.0.035',
            'FirmwareCode': 35,
            'SystemTimestamp': 35000,
            'RequestTimestamp': 1648618952,
            'Timestamp': 1648618952,
            'Brand': 'HITACHI',
            'max_temp': 32,
            'min_temp': 16
        }

        support = JciHitachiAWSStatusSupport(raw_ac_support)

        assert support.status == processed_ac_support
        assert len(processed_ac_support) == len(raw_ac_support) + 3  # `Brand` `max_temp` `min_temp`
    
    def test_str2id(self):
        pass
        # TODO: complete this