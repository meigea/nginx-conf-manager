# coding:utf-8
from django.db import models


class LoadBalanceConfig(models.Model):
    proxy_server = models.CharField(u"负载均衡主机", max_length=155, default="http://localhost:80")
    proxy_stat = models.CharField(u"负载均衡状态", max_length=155, default="down")
    upstream_name = models.CharField(u"所属的负载集合名", max_length=155, default="test_fz")

    def save(self, *args, **kwargs):
        try:
            super(LoadBalanceConfig, self).save(*args, **kwargs)
        finally:
            from phaser1.api.fmg.nginx_txt.v11.conf_v11 import set_upstrem_file
            set_upstrem_file()


class ProxySetting(models.Model):
    location_rx = models.CharField(u"Url路由设置", max_length=33, default="/")
    load_balance_name = models.CharField(u"负载均衡名称", max_length=33, default="") ## 默认不开启负载均衡
    proxy_pass = models.CharField(u"反向代理", max_length=155, default="127.0.0.1")
    proxy_host = models.CharField(u"反向代理主机设置", max_length=55, default="$host:$server_port")
    proxy_cache = models.BooleanField(u"开启缓存策略", default=True)


class WebServerHost(models.Model):
    server_port = models.IntegerField(u"服务端口", default=80)
    servername = models.CharField(u"规则所在文件名", max_length=155, default="127.0.0.1")

    tid = models.IntegerField(u"错误模板方案编号", default=2) ## 错误模板方案编号, 增强版放
    ssl = models.BooleanField(u"开启https", default=False)
    modsecurity = models.BooleanField(u"开启防护", default=True)
    antiTheft_chain = models.BooleanField(u"开启防盗链", default=False)
    proxy_settings = models.ManyToManyField(ProxySetting, verbose_name='代理设置')

    config_name = models.CharField(u"配置名称", max_length=155, default="Web基础服务主机")
    server_desc = models.CharField(u"服务描述", max_length=155, default="127.0.0.1")

    def save2txt(self, *args, **kwargs):
        from phaser1.api.fmg.nginx_txt.v11.conf_v11 import get_vhost_configtxt
        get_vhost_configtxt(host_config=self)






