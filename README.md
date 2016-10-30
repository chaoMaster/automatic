# automatic
  # dedicated REMEDY


# 脚本参数说明：
  -h ———— 帮助文档
  
  -c ———— 配置文件路径

# 注意事项：
  使用前请下载 chrome 驱动，驱动详情：http://blog.csdn.net/chaomaster/article/details/52963265

  脚本启动时，使用 -c 参数指定配置文件, repositories 中有配置文件样例（config.ini）
  
  由于 remedy 网站不可重复登录，所以脚本退出时务必先将 remedy 账号注销登录，以免下次使用时出现登录异常。

  使用时请确保参数中输入的配置文件路径正确。
  
# 更新日志
  v1.0 ------
        完成基础流程设计
     
  v1.1 ------
        添加过滤功能：主要过滤测试 ticket

  v1.2 ------
        添加配置文件，更换启动方式为配置文件启动
        
        配置文件格式：（以 config.ini 命名）请将 remedy 登录信息以及本地 chrome 驱动路径填写在配置文件中
```
            [info]
            username = xxxxx
            password = ******
            driverpath = /xxx/xxxx/chromedriver
```
