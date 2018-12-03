import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains





def ease_out_expo(x):
    if x == 1:
        return 1
    else:
        # 这是一个时间跟距离的函数
        return 1 - pow(2, 10*x)

def get_tracks(distance, seconds, ease_func):
    tracks = [0]
    offsets = [0]
    for t in np.arange(0.0, seconds, 0.1):
        # t 表示每隔几秒  假如是 0.1 秒  除总的时间  乘 总的距离距离
        # 每次移动 上面函数的 距离， offsets 列表 是所有的距离
        offset = round(ease_func(t/seconds) * distance)
        # 那这个tracks 表示什么？ 现在的offset（距离） 减去 上一次 的 距离
        # tracks 代表每次移动的距离
        tracks.append(offsets[-1] - offset)
        # offsets.append(offset)
        # 这个tracks
    print(tracks)
    return tracks

# get_tracks() 方法可以根据滑块的偏移，需要的时间（相对时间，并不是准确时间）
# 以及要采用的缓动函数生成拖动轨迹，然后可以通过下面的方法调用

def drag_and_drop(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    # 获取滑动条的大小
    span_background = driver.find_element_by_css_selector('#nc_1__scale_text > span')
    span_background_size = span_background.size
    print(span_background_size)  # {'height': 32, 'width': 300}


    # # # 获取滑块的位置
    button = driver.find_element_by_css_selector('#nc_1_n1z')
    button_location = button.location
    print(button_location)  # 滑块位置的x y 坐标 {'x': 314, 'y': 262}


    # x_ 是滑动条的长度
    # y 是滑块的 y 坐标


    # 这个为什么这样写？ 看不懂

    x_location = span_background_size['width']
    y_location = button_location['y']
    time.sleep(2)


    # 现在要给Y 写一个循环， 写一个简单的循环
    # 这个能滑过去，但是速度很快
    # ActionChains(driver).drag_and_drop_by_offset(button, x_location, y_location).perform()


    y = y_location
    tracks = get_tracks(y, 50, ease_out_expo)
    print('模拟登录函数执行完毕')
    ActionChains(driver).click_and_hold(button).perform()
    print('准备滑动')
    for x in tracks:
        # print(x)
        ActionChains(driver).move_by_offset(x, 0).perform()
    ActionChains(driver).pause(0.5).release().perform()
    print('滑动完成，准备释放鼠标')


