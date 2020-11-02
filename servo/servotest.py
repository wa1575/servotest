import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685
# 서보모터 테스트 코드
# SG92R를 컨트롤하기 위한 클래스
class SG90_92R_Class:
    # mPin : GPIO Number (PWM)
    # mPwm : PWM컨트롤러용 인스턴스
    # m_Zero_offset_duty

    def __init__(self, Channel, ZeroOffset):
        self.mChannel = Channel
        self.m_ZeroOffset = ZeroOffset

        # Adafruit_PCA9685 초기화
        # address : PCA9685의 I2C Channel 0x40
        self.mPwm = Adafruit_PCA9685.PCA9685(address = 0x40)
   
        self.mPwm.set_pwm_freq(50)

    # 서보모터 위치 설정
    def SetPos(self, pos):
        pulse = (650 - 150) * pos / 180 + 150 + self.m_ZeroOffset
        self.mPwm.set_pwm(self.mChannel, 0, int(pulse))

    # 종료처리
    def Cleanup(self):
        # 서보모터를 90도로 재설정
        self.SetPos(90)
        time.sleep(1)

# 여기가 시작하는 메인 입니다.
if __name__ == '__main__':
    Servo0 = SG90_92R_Class(Channel = 0, ZeroOffset = -10)
    Servo4 = SG90_92R_Class(Channel = 4, ZeroOffset = -10)
 

    try:
        while True:
            Servo0.SetPos(0)
            Servo4.SetPos(0)

            time.sleep(1)
            Servo0.SetPos(90)
            Servo4.SetPos(90)

            time.sleep(1)
            Servo0.SetPos(180)
            Servo4.SetPos(180)
 
            time.sleep(1)
            Servo0.SetPos(90)
            Servo4.SetPos(90)

            time.sleep(1)

    # Ctrl + C키를 누르면 종료 됩니다.
    except KeyboardInterrupt:
        print("Ctrl + C")

    except Exception as e:
        print(str(e))

    finally:
        Servo0.SetPos(0)
        Servo4.SetPos(0)

        Servo0.Cleanup()
        Servo4.Cleanup()

        print("exit program")