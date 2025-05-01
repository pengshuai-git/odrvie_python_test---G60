import pyautogui
import time
import keyboard  # 用于监听键盘事件

def simulate_mouse_motor():
    # 定义屏幕上的两个位置（对应角度 330 和 30）
    position_330 = (250, 450)  # 330 对应的屏幕坐标
    position_30 = (450, 450)  # 30 对应的屏幕坐标

    position_330 = (450,750)  # 30 对应的屏幕坐标

    print("程序运行中，按下 'C' 键退出程序。")
    A=0
    while A<100:
        # 检查是否按下 'C' 键
        if keyboard.is_pressed('c'):
            print("检测到 'C' 键，程序退出。")
            break

        # 移动到 330 的位置并点击
        pyautogui.moveTo(position_330[0], position_330[1], duration=0.1)
        print("Moved to 330 position")
        pyautogui.click()  # 左键点击
        time.sleep(0.5)  # 间隔 1 秒

        if keyboard.is_pressed('c'):
            print("检测到 'C' 键，程序退出。")
            break

        # 移动到 30 的位置并点击
        pyautogui.moveTo(position_30[0], position_30[1], duration=0.1)
        print("Moved to 30 position")
        pyautogui.click()  # 左键点击
        time.sleep(0.5)  # 间隔 1 秒
        A=A+1
        print("循环次数：", A)

if __name__ == "__main__":
    simulate_mouse_motor()