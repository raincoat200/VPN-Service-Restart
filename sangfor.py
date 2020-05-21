#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
# @Time    : 2020/4/2
# @Author  : raincoat200
# @E-mail  : raincoat200@qq.com
# @Site    : https://github.com/raincoat200/
# @File    : sangfor.py
# @Software: PyCharm
"""
import tkinter as tk
import easygui
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import  subprocess
import  re
import netifaces
import threading

def super_ping(serverip,nums):
    #调用系统自带的ping.exe实现ip，返回值为
    p = subprocess.Popen(["ping.exe",serverip,"-n",nums], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    while p.poll() is None:
        line = p.stdout.readline().decode('gbk')
        if  len(line) :  # 判断是否是空行
            print(str.replace(line,'\n',''))
    out = p.stdout.read().decode('gbk')
    regLost = r'\(\d+%'
    regMinimum = u'Minimum = \d+ms|最短 = \d+ms'
    regMaximum = u'Maximum = \d+ms|最长 = \d+ms'
    regAverage = u'Average = \d+ms|平均 = \d+ms'
    lost = re.search(regLost, out)
    minimum = re.search(regMinimum, out)
    maximum = re.search(regMaximum, out)
    average = re.search(regAverage, out)
    if lost:
        lost = lost.group()[1:]
    if minimum:
        minimum = list(filter(lambda x: x.isdigit(), minimum.group()))
    if maximum:
        maximum = list(filter(lambda x: x.isdigit(), maximum.group()))
    if average:
        average = list(filter(lambda x: x.isdigit(), average.group()))
    lost = int(str.replace(lost,'%',''))
    if lost!=100:
        minimum = int("".join(minimum))
        maximum = int("".join(maximum))
        average = int("".join(average))
        ## Minimum = 37ms, Maximum = 38ms, Average = 37ms
        ## 最短 = 37ms，最长 = 77ms，平均 = 48ms
    else:
        ##100%丢失
        minimum = 999
        maximum = 999
        average = 999
    global report
    report =report+ '[%-10s] :  丢包率 %3d%%，最短 %3dms，最长 %3dms，平均 %3dms' % (serverip, lost, minimum, maximum, average)+'\n'
    if minimum>20 or maximum>1000:
        result=False
    else:
        result=True
    return (result)

def super_ipconfig():
    global routingGateway
    global routingIPAddr
    global routingNicMacAddr
    routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
    routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]
    for interface in netifaces.interfaces():
        if interface == routingNicName:
            routingNicMacAddr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            try:
                routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                #routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
            except KeyError:
                pass
    display_format = '%-10s %-25s'
    print (display_format % ("网关IP:", routingGateway))
    print (display_format % ("本机MAC:", routingNicMacAddr.upper()))
    print (display_format % ("本机IP:", routingIPAddr))
    #print (display_format % ("Routing IP Netmask:", routingIPNetmask))
    return routingGateway

class Display:
    def __init__(self):
        self.frm = tk.Tk()
        self.frm.title('营业部VPN重启工具 V1.0')
        self.frm.geometry("600x470")
        self.frm.resizable(False, False)
        menubar = tk.Menu(self.frm)
        menubar.add_cascade(label='使用说明', command=self.help)
        #menubar.add_cascade(label='关于作者', command=self.frm.quit)
        #menubar.add_cascade(label='退出程序', command=self.frm.quit)
        self.frm.config(menu=menubar)

        super_ipconfig()
        self.label1 = tk.Label(self.frm,text='防  火  墙  IP:')
        self.label1.place(x=10,y=10)
        self.var_firewall_ip = tk.StringVar()
        self.var_firewall_ip.set(routingGateway)
        self.entry1 = tk.Entry(self.frm,width=30,textvariable=self.var_firewall_ip)
        self.entry1.place(x=100,y=10)

        self.label2 = tk.Label(self.frm,text='管     理    员:')
        self.label2.place(x=10,y=40)
        self.var_usr_name = tk.StringVar()
        self.var_usr_name.set('admin')
        self.entry2 = tk.Entry(self.frm,width=30,textvariable=self.var_usr_name)
        self.entry2.place(x=100,y=40)

        self.label3 = tk.Label(self.frm,text='密            码:')
        self.label3.place(x=10,y=70)
        self.password = tk.StringVar()
        self.entry3 = tk.Entry(self.frm,width=30,textvariable=self.password, show='*')
        self.entry3.place(x=100,y=70)

        self.label4 = tk.Label(self.frm,text='本机 IP/MAC:   '+routingIPAddr+" / "+routingNicMacAddr.upper())
        self.label4.place(x=10,y=100)

        self.label5 = tk.Label(self.frm, text='    '*9+' Powered by Python    |    Design by:raincoat200@qq.com',font= ("Microsoft JhengHei UI Light", 10))
        self.label5.place(y=445)

        self.text = tk.Text(self.frm,bg='black',foreground = 'white')
        self.text.tag_configure("stderr")
        self.text.place(x=10,y=130)

        sys.stdout = TextRedirector(self.text, "stdout")

        self.btn1 = tk.Button(self.frm,text=' 网络诊断 ',command=self.netstat)
        self.btn1.place(x=400,y=20)
        self.btn2 = tk.Button(self.frm, text=' 重启VPN服务 ', command=self.run)
        self.btn2.place(x=400, y=65)
        self.btn0 = tk.Button(self.frm,text=' 退出 ',command=self.frm.quit)
        self.btn0.place(x=500,y=20)
        #self.netstat() #默认启动
    def help(self):
        #showinfo(title='使用说明', message='使用说明')
        text='''
适配深信服VPN防火墙 AC6.1版本。因官方组件仅允许IE浏览器登陆操作，故不支持无痕模式。本程序实现以下功能：

1、IPCONFIG 获取网关 IP 。\n
2、采用PING包检测两条VPN链路丢包率。\n
3、SELENIUM网络爬虫登陆 FIREWALL 。\n
4、依次点击 VPN 配置-> DLAN 运行状态->停止服务->开始服务。\n
5、预留定时计划任务，检测丢包率达到阈值自动重启功能。 \n
6、本程序开源，代码公布于GITHUB主页www.github.com/raincoat200,欢迎助力。\n
'''
        easygui.msgbox(text,'使用说明')

    def diagnose(self):
        global report
        report=''
        print('->')
        print('->'+time.strftime("%Y-%m-%d %H:%M:%S"))
        print('->网络状况诊断中,请稍等')
        super_ping('10.88.2.50','10')
        super_ping('10.0.2.143','10')
        print('-' * 64)
        print('-> ' +'\n')
        print(report)
        print('->')
        print('->'+ time.strftime("%Y-%m-%d %H:%M:%S"))
        print('->网络诊断完成')

    def netstat(self):
        # 创建新线程
        self.thread1 = threading.Thread(target=self.diagnose)
        self.thread2 = threading.Thread(target=self.check)
        self.thread1.setDaemon(True)
        self.thread2.setDaemon(True)
        self.thread1.start()
        self.thread2.start()

    def check(self):
        while True:
            if self.thread1.is_alive():
                self.btn1['state'] = tk.DISABLED
            else:
                self.btn1['state'] = tk.NORMAL
            self.frm.update()

    def run(self):
        print('->')
        print('->' + time.strftime("%Y-%m-%d %H:%M:%S"))
        print('->准备重启VPN服务'+'\n')
        self.thread3 = threading.Thread(target=self.super_restart)
        self.thread3.setDaemon(True)
        self.thread3.start()

    def super_restart(self):
        user_password = self.entry3.get()
        if len(user_password) == 0:
            text="密码不能为空，请输入防火墙密码。\n\n如需帮助，请联系网络组老师。\n\nQ群166046974"
            print("密码长度:"+str(len(user_password)))
            easygui.msgbox(text, '密码异常')
            sys.exit()
        DriverPath = r'.\IEDriverServer.exe'
        ie_options = webdriver.IeOptions()
        ie_options.add_argument('--disable-gpu')
        ie_options.add_argument('--no-sandbox')
        ie_options.add_argument('--disable-dev-shm-usage')
        ie_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko")
        #driver = webdriver.Ie(executable_path=DriverPath,options=ie_options)
        driver = webdriver.Ie(options=ie_options)
        driver.get('https://' + routingGateway)
        time.sleep(3)
        driver.get("javascript:document.getElementById('overridelink').click();")

        inputwd = driver.find_element_by_id("user")
        inputwd.clear()  # 清楚文本框里的内容
        inputwd.send_keys('admin')  # 输入用户名
        inputwd = driver.find_element_by_id("password")
        inputwd.clear()  # 清楚文本框里的内容
        inputwd.send_keys(user_password)  # 输入密码
        time.sleep(1)
        but = driver.find_element_by_id('button')
        but.click()  # 输入回车键  but.click()  #点击登陆按钮
        time.sleep(1)
        try:
            WebDriverWait(driver, 15, 1).until(EC.title_contains('营业部'))
        except:
            print('->登陆失败，请检查密码是否正确或网络是否正常。' + '\n')
            sys.exit()
        print('->登陆成功' + '\n')
        time.sleep(1)
        inputwd = driver.find_element_by_id("ext-gen110")  # VPN配置
        inputwd.click()

        try:
            WebDriverWait(driver, 10, 1).until(lambda the_driver: the_driver.find_element_by_link_text("DLAN运行状态"),
                                               '失败')
        except Exception as e33:
            print(e33)
        inputwd = driver.find_element_by_link_text("DLAN运行状态")
        inputwd.click()
        time.sleep(5)
        try:
            # 切换到frame内容页
            iframe = driver.find_elements_by_tag_name("iframe")[0]
            WebDriverWait(driver, 10, 1).until(EC.frame_to_be_available_and_switch_to_it(iframe), 'frame失败')
        except Exception as e33:
            print(e33)
        try:
            WebDriverWait(driver, 10, 1).until(lambda the_driver: the_driver.find_element_by_class_name("font-blue"),
                                               'status失败')  # 运行中 状态
        except Exception as e33:
            print(e33)
        # 停止服务
        driver.execute_script("$('.buttons2').click()")
        time.sleep(1)
        dig_alert = driver.switch_to.alert
        time.sleep(1)
        dig_alert.accept()
        print('->停止服务成功' + '\n')
        time.sleep(3)
        try:
            WebDriverWait(driver, 10, 1).until(lambda the_driver: the_driver.find_element_by_class_name("font-red"),
                                               'buttons失败')  # 已停止 状态
        except Exception as e33:
            print(e33)
        # 开始服务
        driver.execute_script("$('.buttons2').click()")
        print('->启动中' + '\n')
        time.sleep(3)
        for i in range(60):
            # 刷新按钮
            driver.execute_script("$('.refresh').click()")
            time.sleep(3)
            try:
                driver.find_element_by_class_name("font-blue")
            except Exception as e33:
                # print(e33)
                print('->')
            else:
                driver.execute_script("$('.refresh').click()")
                break
        print("->重启服务成功" + '\n')
        time.sleep(3)
        driver.close()
        driver.quit()
        self.netstat()

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")
        self.widget.see(tk.END)

if __name__ == '__main__':
    report = ''
    D = Display()
    tk.mainloop()