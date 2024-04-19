将解压后的文件夹放在YOLOV5文件夹下
YOLOV5/DetectGUI

点击 "安装环境.bat" (默认装在base) 右键用记事本打开，更改为你的conda环境名，例如 "rv_vision"
Ctrl + S 保存
双击 "安装环境.bat", 自动安装依赖包

点击 "start.bat" (默认在base中打开) 右键用记事本打开，更改为你的conda环境名，并保存
双击 "start.bat" 运行脚本

点击 "选项" 可以更改所使用的 .pt模型, 可以改为自己炼制的
(默认使用 "yolov5s.pt", 环境中如果没有会自动到github下载, 很慢，不推荐)
打包中附带 "yolov5s.pt", "yolov5n.pt" 需要把它们放到 "YOLOV5/" 根目录下才能读取

打开 "log/application.log" 日志文件, 可以看到历史操作

打开 "config/config.ini" 配置文件, 可以修改默认模型，图片和视频路径

图形界面关闭后，脚本命令行仍会驻留，若需自动关闭，请在代码中添加 "sys.exit(app.exec_())" ，或者删除.bat脚本中的pause

每次启动脚本，都会预先加载模型，若不需要这个功能或者嫌慢，可修改"__init__"中的 "self.model = None"