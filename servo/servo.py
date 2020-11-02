import time
import Adafruit_PCA9685
import RPi.GPIO as GPIO

#목표지점에 착륙할 때마다 1씩 증가시킨다고 가정 
dcnt = 0;


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
        # 50Hz로 설정하셔야 하지만 60Hz로 하시는게 좀더 좋습니다.
        self.mPwm.set_pwm_freq(60)

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
    #Servo8 = SG90_92R_Class(Channel = 8, ZeroOffset = -10)
    #Servo12 = SG90_92R_Class(Channel = 12, ZeroOffset = -10)

    try:
        while True:
            Servo0.SetPos(0)
            Servo4.SetPos(0)
            #Servo8.SetPos(0)
            #Servo12.SetPos(0)
            time.sleep(1)
            if dcnt % 2 ==  1 : # 첫번째 지점 도착 시 1번째 110도까지 
                Servo0.SetPos(100)
                print(" ** First Delivery complete ** ")
                time.sleep(3) # 동작 끝날때까지 대기 

            
            elif dcnt % 2 ==  0 : # 두번째 지점 도착 시  2번째 110도까지
                Servo4.SetPos(100)
                print(" ** Second Delivery complete ** ")
                time.sleep(3) # 동작 끝날때까지 대기 

            
            time.sleep(1)


    # Ctrl + C키를 누르면 종료 됩니다.
    except KeyboardInterrupt:
        print("Ctrl + C")

    except Exception as e:
        print(str(e))

    finally:
        dcnt = 0; # dcnt 초기화 
        Servo0.SetPos(0)
        Servo4.SetPos(0)

        Servo0.Cleanup()
        Servo4.Cleanup()

        print("#exit Delivery#")