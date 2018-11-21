# coding:utf-8

## 根据对象生成 conf, 并且取名字
import os

from phaser1.models import WebServerHost, ProxySetting, LoadBalanceConfig
from phaser1.api.fmg.file_config import NginxBaseDir
from phaser1.api.fmg.nginx_txt.v11.cfg_v11 import waf_help_txt

from phaser1.api.fmg.nginx_txt.v11.v11_utils import NginxConf

def set_upstrem_file():
    upstream_names = set([x.upstream_name for x in LoadBalanceConfig.objects.all()])
    upstream_str = "\n"
    for upstream_name in upstream_names:
        upstream_str += "upstrem {}".format(upstream_name) + "{\n"
        for lbc in LoadBalanceConfig.objects.filter(upstream_name=upstream_name):
            upstream_str += " "*4 +lbc.proxy_server + " " + lbc.proxy_stat + ";\n"
        upstream_str += "}\n\n"

    with open(os.path.join(NginxBaseDir, "upstreams.conf"), "w+", encoding="utf-8") as f:
        f.write(upstream_str)
        f.close()
    return True

def set_waf_help_conf():
    with open(os.path.join(NginxBaseDir, "waf-help.conf"), "w+", encoding="utf-8") as f:
        f.write(waf_help_txt)
        f.close()
    return True


def get_vhost_configtxt(host_config, CONFNAME_BY_PORT=True):
    conf_settings = dict(
        local_server_port=host_config.server_port,
        server_name=host_config.servername,

        tid=int(host_config.tid),
        ssl="" if host_config.ssl else "#",
        modsec="" if host_config.modsecurity else "#",
        start_fdl=host_config.antiTheft_chain,
        config_name=host_config.config_name,
        server_desc=host_config.server_desc,
        cc="" if host_config.antiTheft_chain else "#",
    )

    conf_settings["no_ssl"] = "#" if host_config.ssl else ""

    _local_cfgs = []
    # print([x.proxy_pass for x in host_config.proxy_settings.all()])
    for proxy_setting in host_config.proxy_settings.all():
        local_cfg = dict(
            url_begin=proxy_setting.location_rx,
            load_balance_name=proxy_setting.load_balance_name,
            proxy_server=proxy_setting.proxy_pass,
            server_host=proxy_setting.proxy_host,
            proxy_cache=proxy_setting.proxy_cache,
        )
        _local_cfgs.append(local_cfg)
    conf_settings["location_cfgs"] = _local_cfgs

    if CONFNAME_BY_PORT:
        _local_conf_name = str(conf_settings["local_server_port"])
    else:
        _local_conf_name = conf_settings["config_name"]

    with open(os.path.join(NginxBaseDir, "vhost", _local_conf_name) + ".conf", "w+", encoding="utf-8") as f:
        f.write(NginxConf(cfg=conf_settings).get_server_content())
        f.close()


## 根据host来把所有的主机部署上
def init_all_confgs():
    for host_config in WebServerHost.objects.all():
        get_vhost_configtxt(host_config)










