# automatic
  # dedicated REMEDY


# 注意事项：
  使用前请下载 chrome 驱动，驱动详情：http://blog.csdn.net/chaomaster/article/details/52963265

  使用脚本前必须创建配置文件（文件名 config.ini）,且需要将配置文件和脚本放在同一目录。必须使用 config.ini 作为文件名
  （FOR MAC ：如果需要双击启动脚本，请将配置文件放一份在自己的 home 下）
  
  
  由于 remedy 网站不可重复登录，所以脚本退出时务必先将 remedy 账号注销登录，以免下次使用时出现登录异常。

  
# 更新日志
  v1.0 ------
        完成基础流程设计
     
  v1.1 ------
        添加过滤功能：主要过滤测试 ticket

  v1.2 ------
        添加配置文件，更换启动方式为配置文件启动
        
        配置文件格式：（以 config.ini 命名）请将 remedy 登录信息以及本地 chrome 驱动路径填写在配置文件中
```objc
            [info]
            username = xxxxx
            password = ******
            driverpath = /xxx/xxxx/chromedriver
            audiopath = file:///Users/xxxx/Desktop/1234.mp3
```
  v1.3 ------
        新增提醒功能模块
        
        添加网络监测功能：如果检测断网等情况，播放音乐提醒
        
        添加提醒功能：脚本运行期间，如果发生不能自动处理的意外，播放音乐提醒

  v2.0 ------
  
         修复若干 bug 
         
         新增 windows 支持，修复之前版本 windows 网络监控模块不可用 bug ，可下载对应系统的二进制文件双击运行
         
         新增 脚本处理日志导出功能，即脚本运行过程中处理的信息会导出到文件 ticket.log
         
