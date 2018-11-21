# coding:utf-8

## 通过输入参数, 返回正确的 nginx 模板
from .cfg_v11 import *

class NginxConf():
    def __init__(self, cfg=None, **kwargs):
        self.cfg = cfg
        self.space="" ## 格式的基础缩进
        self.tpace= " "*4 ## 格式的基础缩进
        self.error_nums = [400, 401, 402, 403, 404, 500, 501, 502, 503] ## 自定义错误码设定
        self.cache_name="cya_waf_cache"

    ##  核心函数
    def get_server_content(self):
        server_content = self.space + "server " + "{\n" + self.space + self.tpace
        server_content += ("\n" + self.space + self.tpace ).join( server_content_head.format(**self.cfg).split("\n") )
        server_content += "\n" + NginxConf(cfg=self.cfg).get_error_page_settings() +"\n"
        server_content += self.get_location_conf(**self.cfg)
        if self.cfg["start_fdl"]:
            server_content += self.get_fdl_str()
        server_content +="\n"+ self.space + "}\n"
        return server_content


    def get_location_conf(self, **kwargs):
        res_localtion_strs = ""
        for location_cfg in kwargs["location_cfgs"]:
            if "url_begin" not in location_cfg.keys():
                continue
            string_demo = self.space + self.tpace + "location {location_url} ".format(
                location_url=location_cfg["url_begin"]) + "{\n"

            ### 开始判断location的各种设置内容
            if location_cfg["load_balance_name"] == "":
                ## 缓存策略全部默认开启
                custom_error = "proxy_intercept_errors on;\n"
                proxy_cache = "proxy_cache {};".format(self.cache_name)
                start_cache_strategy = ""

                if not location_cfg["proxy_cache"]:
                    proxy_cache = ""
                    start_cache_strategy = "#"

                pre_str = location_proxy.format(
                    proxy_cache=proxy_cache,
                    server_host=location_cfg["server_host"],
                    proxy_server=location_cfg["proxy_server"],
                    cache_cn=start_cache_strategy,  ## 策略
                    custom_error=custom_error, ## 自定义错误页面开启
                )
                res_str = ("\n" + self.space + self.tpace * 2).join(pre_str.split("\n"))
                string_demo += res_str
            else:
                ## 开启负载均衡
                custom_error = "proxy_intercept_errors on;\n"
                proxy_cache = "proxy_cache {};".format(self.cache_name)
                start_cache_strategy = ""

                if not location_cfg["proxy_cache"]:
                    proxy_cache = ""
                    start_cache_strategy = "#"

                pre_str = location_proxy.format(
                    proxy_cache=proxy_cache,
                    server_host=location_cfg["server_host"],
                    proxy_server="http://" + location_cfg["load_balance_name"],
                    cache_cn=start_cache_strategy,  ## 策略
                    custom_error=custom_error, ## 自定义错误页面开启
                )
                res_str = ("\n" + self.space + self.tpace * 2).join(pre_str.split("\n"))
                string_demo += res_str


            string_demo += "\n" + self.space + self.tpace * 1 + "}\n\n"

            res_localtion_strs += string_demo
        return res_localtion_strs

    def get_fdl_str(self):
        return "\n" + self.space + self.tpace + ("\n"+self.space+self.tpace).join(
            fdl_partern.format(**self.cfg).split("\n")).replace("$%^", "{").replace("^%$","}")

    def get_error_page_settings(self, tid=6):
        error_page_str = ""
        error_nums = self.error_nums
        error_basesetting_partern = self.space + self.tpace + "error_page {error_num} /error_pages/{tid}/{error_num}.html;" +"\n"
        for error_num in error_nums:
            error_page_str += error_basesetting_partern.format(
                error_num=error_num,
                tid=tid
            )
        return error_page_str









