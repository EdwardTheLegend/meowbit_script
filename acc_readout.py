from pyb import wfi, delay
from empty import EmptyScript


class AccReadoutScript(EmptyScript):
    name = "acc_readout"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def main(self):
        iterations = 0
        self.display_all_acc()
        while True:
            wfi()

            # check if the user wants to exit
            if self.sensor.btnValue("b"):
                break

            iterations += 1

            if iterations == 200:
                iterations = 0
                self.display_all_acc()

            delay(10)

    def display_all_acc(self):
        # get the acceleration data
        acc_x, acc_y, acc_z = (
            self.sensor.acc_x(),
            self.sensor.acc_y(),
            self.sensor.acc_z(),
        )

        # get the gyroscope data
        gyro_x, gyro_y, gyro_z = (
            self.sensor.gyro_x(),
            self.sensor.gyro_y(),
            self.sensor.gyro_z(),
        )

        # get the pitch and roll
        pitch, roll = self.sensor.get_pitch(), self.sensor.get_roll()

        # get the gesture
        gesture = self.sensor.gesture()

        # display all info
        self.screen.fill((255, 255, 255), update=False)
        display_text = (
            "acc_x: %.2f\nacc_y: %.2f\nacc_z: %.2f\n\ngyro_x: %.2f\ngyro_y: %.2f\ngyro_z: %.2f\n\npitch: %.2f\nroll: %.2f\n\ngesture: %s"
            % (
                acc_x,
                acc_y,
                acc_z,
                gyro_x,
                gyro_y,
                gyro_z,
                pitch,
                roll,
                gesture,
            )
        )
        # print(display_text)
        self.screen.text(text=display_text, x=5, y=5, color=(255, 0, 0), update=False)

        # update the screen
        self.screen.refresh()
