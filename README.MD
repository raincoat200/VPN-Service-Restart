<h1>营业部VPN重启工具 v1.0</h1>

##使用说明：
1. 适配深信服VPN防火墙 AC6.1版本。
2. 官方组件仅允许IE浏览器登陆操作（IE不支持无痕模式）。
3. 本程序实现以下功能：
<ul>
<li>IPCONFIG 获取网关 IP 。</li>
<li>采用PING包检测两条VPN链路丢包率。</li>
<li>SELENIUM网络爬虫登陆 FIREWALL 。</li>
<li>依次点击 VPN 配置-> DLAN 运行状态->停止服务->开始服务。</li>
<li>预留定时计划任务，检测丢包率大于指定数值自动重启功能。</li>
</ul>

---

##脚本环境：
1. python 3.8
2. ie 11 浏览器 11.864.17763.0（需下载对应浏览器chromedriver驱动）
3. win10 64 bit
4. SANGFOR AC6.1

---