import math
from pyb import I2C, ADC, Pin, delay
from micropython import const

ACC_REST = const(400)
ACC_SHAKE = const(1600)


class Sensor:
    def __init__(self):
        self.iic = I2C(1)
        self.iic.init()
        self.addr = 0x68
        self.iic.send(bytearray([107, 0]), self.addr)
        self.adcLight = ADC("LIGHT")
        self.adcTemp = ADC("TEMP")
        self._accUpdate()
        # btns
        self.btn_LEFT = Pin("LEFT", Pin.IN, Pin.PULL_UP)
        self.btn_UP = Pin("UP", Pin.IN, Pin.PULL_UP)
        self.btn_DOWN = Pin("DOWN", Pin.IN, Pin.PULL_UP)
        self.btn_RIGHT = Pin("RIGHT", Pin.IN, Pin.PULL_UP)
        self.btn_BTNA = Pin("BTNA", Pin.IN, Pin.PULL_UP)
        self.btn_BTNB = Pin("BTNB", Pin.IN, Pin.PULL_UP)

    def _accUpdate(self):
        imu = self.iic.mem_read(14, self.addr, 0x3B)
        self.imu = imu
        # map to -1024~1024
        self.x = self.bytes_toint(imu[0], imu[1]) / 16
        self.y = self.bytes_toint(imu[2], imu[3]) / 16
        self.z = self.bytes_toint(imu[4], imu[5]) / 16
        self.gx = self.bytes_toint(imu[8], imu[9])
        self.gy = self.bytes_toint(imu[10], imu[11])
        self.gz = self.bytes_toint(imu[12], imu[13])
        return self.imu

    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return -(((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def _adc2temp(
        self, adcValue, res=10000, beta=3300, norm=25.0, normread=10000, zero=273.5
    ):
        sensor = 4096.0 * res / adcValue - res
        value = (
            1.0 / ((math.log(sensor / normread) / beta) + (1.0 / (norm + zero)))
        ) - zero
        return int(value)

    def getTemp(self, fa=0):
        ce = self._adc2temp(self.adcTemp.read())
        if fa:
            return (ce * 1.8) + 32
        return ce

    def getIntensity(self):
        return self.adcLight.read()

    def acc_x(self):
        self._accUpdate()
        return self.x

    def acc_y(self):
        self._accUpdate()
        return self.y

    def acc_z(self):
        self._accUpdate()
        return self.z

    def _updatePR(self):
        self.roll = math.atan2(self.x, -self.z)
        self.pitch = math.atan2(
            self.y, (self.x * math.sin(roll) - self.z * math.cos(roll))
        )

    def gyro_x(self):
        self._accUpdate()
        return self.gx

    def gyro_y(self):
        self._accUpdate()
        return self.gy

    def gyro_z(self):
        self._accUpdate()
        return self.gz

    def pitch(self):
        self._accUpdate()
        self._updatePR()
        return 360 * self.pitch / 2 / math.pi

    def roll(self):
        self._accUpdate()
        self._updatePR()
        return 360 * self.roll / 2 / math.pi

    def gesture(self, gesCheck=None):
        self._accUpdate()
        shakeDect = False
        if (self.x < -ACC_SHAKE) or (self.x > ACC_SHAKE):
            shakeDect = True
        if (self.y < -ACC_SHAKE) or (self.y > ACC_SHAKE):
            shakeDect = True
        if (self.z < -ACC_SHAKE) or (self.z > ACC_SHAKE):
            shakeDect = True
        detGes = None
        self.gF = self.x * self.x + self.y * self.y + self.z * self.z
        if shakeDect:
            detGes = "shake"
        elif self.gF < (200 * 200):
            detGes = "freefall"
        elif self.x > 2 * ACC_REST:
            detGes = "tilt_up"
        elif self.x < -2 * ACC_REST:
            detGes = "tilt_down"
        elif self.y > 2 * ACC_REST:
            detGes = "tilt_left"
        elif self.y < -2 * ACC_REST:
            detGes = "tilt_right"
        elif self.z < -2 * ACC_REST:
            detGes = "face_up"
        elif self.z > 2 * ACC_REST:
            detGes = "face_down"
        if gesCheck:
            return detGes == gesCheck
        else:
            return detGes

    def debounce(self, pin):
        for i in range(50):
            if pin.value() != 0:
                return False
            delay(1)
        return True

    def btnValue(self, btn):
        btn = btn.lower()
        if btn == "a":
            if self.debounce(self.btn_BTNA):
                return True
            return False
        elif btn == "b":
            if self.debounce(self.btn_BTNB):
                return True
            return False
        elif btn == "left":
            if self.debounce(self.btn_LEFT):
                return True
            return False
        elif btn == "up":
            if self.debounce(self.btn_UP):
                return True
            return False
        elif btn == "right":
            if self.debounce(self.btn_RIGHT):
                return True
            return False
        elif btn == "down":
            if self.debounce(self.btn_DOWN):
                return True
            return False
