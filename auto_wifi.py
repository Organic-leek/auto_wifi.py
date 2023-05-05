import os
import subprocess
import time

from selenium import webdriver
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class auto_wifi:
    def __init__(self, wifi_name):
        self.wifi_name = wifi_name

    # 连接目标wifi
    def auto_switch_wifi(self):
        count = 3
        cmd = 'netsh wlan connect name={}'.format(self.wifi_name)
        while count:
            try:
                res = os.system(cmd)
                if res == 0:
                    print(self.wifi_name, '连接成功')
                    count = 0
                else:
                    time.sleep(2)
                    print('failed')
                    count -= 1
            except Exception as e:
                print('连接', self.wifi_name, '时出错')

    def wifi_in_range(self):
        count = 3
        while count:
            if self.wifi_SSID in self.wifilist_get():
                self.auto_switch_wifi()
                break
            else:
                time.sleep(1)
                count -= 1
                if count == 0:
                    print('未在wifi范围内')
                    return True

    # 目标wifi的SSID
    def SSID_get(self):
        try:
            wifi_file = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles', wifi_name]).decode('ansi')
            wifi_SSID = re.findall('“(.*)”', wifi_file)[0]
            return wifi_SSID
        except Exception as e:
            print('可能是输入的wifi名错误')

    # 可连接wifi列表
    def wifilist_get(self):
        try:
            result = subprocess.check_output(['netsh', 'wlan', 'show', 'network']).decode('ansi')
            wifilist = re.findall('SSID .{1,2} : (.*)\r\n', result)
            return wifilist
        except Exception as e:
            print(e)

    # wifi连接状态
    def state_get(self):
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('ansi')
        state = re.findall(' 状态.*: (.*)\r\n', result)[0]
        if state == '已断开连接':
            self.wifi_in_range()
        else:
            if state == '已连接':
                SSID_now = re.findall(' SSID.*: (.*)\r\n', result)[0]
                NAME_now = re.findall(' 配置文件.*: (.*)\r\n', result)[0]
                if self.wifi_SSID == SSID_now:
                    print('已连接WiFi：', self.wifi_name)
                else:
                    os.system('netsh wlan disconnect')
                    time.sleep(1)
                    if self.wifi_in_range():
                        time.sleep(1)
                        os.system('netsh wlan connect name={}'.format(NAME_now))
            else:
                print('状态为：', state)
                time.sleep(2)
                self.state_get()

    def main(self):
        self.wifi_SSID = self.SSID_get()
        if self.wifi_SSID:
            self.state_get()

def download_driver():
    pass

def login(times=2):
    try:
        driver = webdriver.Edge()
        driver.get(url)
        time.sleep(int(data[4]))
        html = driver.page_source
        if re.search('登录',html):
            if re.search('domain-list',html):
                s = driver.find_element(By.ID, 'domain')
                Select(s).select_by_value('@cmcc')
            username=driver.find_element(By.ID, 'username')
            username.send_keys(data[2])
            password = driver.find_element(By.ID, 'password')
            password.send_keys(data[3])
            time.sleep(1)
            if re.search('btn btn-block btn-primary',html):
                driver.find_element(By.ID,'login').click()
            if re.search('id="login-account"', html):
                driver.find_element(By.ID,'login-account').click()
            time.sleep(5)
            driver.close()
    except Exception as e:
        print(e)
        if times>0:
            time.sleep(6)
            login(times-1)


if __name__ == '__main__':

    with open('test.txt', 'r') as a:
        data = a.read()
    data = re.findall('“(.*)”', data)
    wifi_name = data[0]
    url = data[1]
    version = next(os.walk(data[5]))[1][0]

    auto_wifi(wifi_name).main()
    login()