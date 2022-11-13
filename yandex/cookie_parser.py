



cookies = "yandexuid=2736705921664023588; _ym_uid=1664023590615010216; _ym_d=1664023591; yuidss=2736705921664023588; i=HJNkS8g/LstlpfQlv22E2fIUt1RZ+qxC8HV9EWcP/Qv9rP72ko0Pk+l1hZ0AZg0UHKui+9eJBzcD+y7SS2pH3VnyYUs=; skid=8709324011665588545; gdpr=0; is_gdpr=0; is_gdpr_b=CN+rNhCMkQEoAg==; _ym_isad=2; _yasc=+MOFCKAgCDU3RG79/hCF0Fn2XoKCf3QnPWobIscMMZxFhwLgsF03if+NWEn8zxeWrzIcxBINMQ==; ymex=1669446518.oyu.2736705921664023588#1980863275.yrts.1665503275#1980863275.yrtsi.1665503275; _ym_visorc=b; Session_id=3:1666854613.5.3.1666718191892:FHtjJQ:d.1.2:1|1704658412.0.2|1704661667.500.0.2:500|1704995762.80476.0.2:80476|1705185795.136422.0.2:136422|5:10177184.560993.vQhVf1Y1wQZTz7ZpoJhcPfDu5dI; sessionid2=3:1666854613.5.3.1666718191892:FHtjJQ:d.1.2:1|1704658412.0.2|1704661667.500.0.2:500|1704995762.80476.0.2:80476|1705185795.136422.0.2:136422|5:10177184.560993.fakesign0000000000000000000; yp=1982078108.multib.1#1982214613.udn.cDrQntC70LXQsyDQntC70LXQsw==#1666940918.yu.2736705921664023588; ys=udn.cDrQntC70LXQsyDQntC70LXQsw==; L=WlFeUQFOenBBbVhzdXpsbFpQQHhUUAYCP0FcCwEUAUETQzsrLww=.1666854613.15143.360908.2684b77b056ee00aac319fcbaaf89ed2; yandex_login=nphne-u6cvcccz"

cookies_array = cookies.split('; ')
json = {}

for cookie in cookies_array:
    key = cookie.split('=')[0]
    value_array = cookie.split('=',1)
    value = ''
    for i in range(len(value_array)):
        if i != 0:
            value = value + value_array[i]

    # print(value)
    json[key] = value

print(json)