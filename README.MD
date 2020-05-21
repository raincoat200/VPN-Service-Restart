<h1>防火墙VPN重启工具 v1.0</h1>

##使用说明：
1.  适配深信服VPN防火墙 AC6.1版本(理论上UI一样均兼容)。
2.  官方组件仅允许IE浏览器登陆操作,不支持chrome firefox浏览器,故IE不支持无痕后台运行模式。
3.  本程序实现以下功能：

    * CMD环境下IPCONFIG 获取网关(防火墙) IP 。
    * 采用PING包检测两条VPN链路丢包率。
    * SELENIUM网络爬虫登陆 FIREWALL  WEB端。
    * 依次点击 VPN 配置-> DLAN 运行状态->停止服务->开始服务。
    * 预留定时计划任务接口，支持检测丢包率达到指定阀值，自动重启功能。

![运行日志截图](https://github.com/raincoat200/VPN-Service-Restart/blob/master/demo/1.png)     

![运行日志截图](https://github.com/raincoat200/VPN-Service-Restart/blob/master/demo/2.png)     

![运行日志截图](https://github.com/raincoat200/VPN-Service-Restart/blob/master/demo/3.png)     

---

##脚本环境：
1.  python 3.8
2.  ie 11 浏览器 11.864.17763.0（需下载对应浏览器iedriver驱动）
3.  win10 64 bit
4.  SANGFOR AC6.1

---