# coding:utf-8

location_proxy = """
{proxy_cache}
proxy_pass {proxy_server};
proxy_redirect off;
proxy_set_header Host {server_host};
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
client_max_body_size 10m;
client_body_buffer_size 128k;
proxy_connect_timeout 90;
proxy_send_timeout 90;
proxy_read_timeout 90;
proxy_buffer_size 64k;
proxy_buffers 32 32k;
proxy_busy_buffers_size 128k;
proxy_temp_file_write_size 128k;

proxy_cache_key $proxy_host$request_uri$cookie_jessionid;
{cache_cn}proxy_cache_valid 200 302 10m;
{cache_cn}proxy_cache_valid 404      1m;
{cache_cn}proxy_cache_valid 500 502  0m;

{custom_error}
"""

server_content_head = """{modsec}modsecurity on;
{modsec}modsecurity_rules_file /etc/nginx/modsecurity.conf;

{no_ssl}listen       {local_server_port};
{ssl}listen       {local_server_port} ssl;
server_name  {server_name};

{ssl}ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
{ssl}ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;
{ssl}ssl_dhparam /etc/ssl/certs/dhparam.pem; #charset koi8-r;

access_log  /var/log/nginx/$host-$server_port.access.log custom;

{cc}limit_req zone=allips burst=5 nodelay;

"""

fdl_partern = """
location ~* \.(gif|jpg|png|jpeg|js|css)$ $%^
    expires     30d;
    valid_referers none blocked {server_name};
    if ($invalid_referer) $%^
      rewrite ^/ http://{server_name}/fangdaolian;
    ^%$
^%$
"""


waf_help_txt = """
proxy_cache_path /tmp/ levels=1:2 keys_zone=cya_waf_cache:10m max_size=10g inactive=60m use_temp_path=off;

log_format  custom '$remote_addr - $remote_user [$time_local] '
'"$request" $status $body_bytes_sent '
'"$http_referer" "$http_user_agent" '
'"$http_x_forwarded_for" $request_id ';

"""