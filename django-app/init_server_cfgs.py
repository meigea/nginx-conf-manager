# coding:utf-8

from phaser1.models import WebServerHost, ProxySetting, LoadBalanceConfig

cfgs = [
    dict(server_port=80,
        config_name="waf",
        servername="waf.test.com 1.test.com",
         proxy_settings=[
            dict(proxy_pass="http://192.168.2.110:9070", location_rx="/"),
            dict(proxy_pass="http://192.168.2.110:8070/WebGoat", location_rx="/WebGoat"),
         ],
    ),
    dict(server_port=3380,
        servername="2.test.com 3.test.com",
        config_name = "site1",
         proxy_settings=[
            dict(load_balance_name="mytestlb", location_rx="/"),
         ],
    ),
]

_demo_load_balance = [
    dict(proxy_server="http://192.168.2.110:9070",
        proxy_stat="weight=20 max_fails=2 fail_timeout=30s",
        upstream_name="mytestlb",
    ),
    dict(proxy_server="http://192.168.2.223:9070",
        proxy_stat="weight=10 max_fails=3 fail_timeout=30s",
        upstream_name="mytestlb",
    ),
    dict(proxy_server="http://192.168.2.113:9070",
        proxy_stat="down",
        upstream_name="mytestlb",
    ),
    dict(proxy_server="http://192.168.2.113:9070",
         proxy_stat="weight=1",
         upstream_name="mytestlb2",
    )
]

def init_load_balance():
    LoadBalanceConfig.objects.all().delete()
    for x in _demo_load_balance:
        LoadBalanceConfig.objects.create(**x)

def init_webhost():
    for cfg in cfgs:
        wsh = WebServerHost()
        wsh.server_port = cfg["server_port"]
        wsh.servername = cfg["servername"]
        wsh.config_name = cfg["config_name"]
        wsh.save()
        
        for x in cfg["proxy_settings"]:
            local_ps = ProxySetting.objects.create(**x)
            wsh.proxy_settings.add(local_ps)


def init_conf_settings():
    LoadBalanceConfig.objects.all().delete()
    WebServerHost.objects.all().delete()
    ProxySetting.objects.all().delete()

    init_load_balance()
    init_webhost()



