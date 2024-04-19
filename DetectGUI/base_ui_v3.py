import configparser
import logging
import sys

from pathlib import Path

import cv2
import torch

from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog

from detect_ui import Ui_MainWindow

from pathlib import Path


# 应用根目录
BASE_PATH = Path(__file__).parent.resolve()

# 创建日志和配置文件夹
CONFIG_PATH = BASE_PATH / 'config'
LOG_PATH = BASE_PATH / 'log'
CONFIG_PATH.mkdir(exist_ok=True)
LOG_PATH.mkdir(exist_ok=True)

# 创建配置文件
def init_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH / 'config.ini')
    if 'Paths' not in config:
        config['Paths'] = {
            'ModelDir': '',
            'ImageDir': '',
            'VideoDir': ''
        }
        with open(CONFIG_PATH / 'config.ini', 'w') as configfile:
            config.write(configfile)
    return config

config = init_config()

def update_config(section, option, new_value):
    # new_value = str(new_value)
    config.set(section, option, new_value)
    with open(CONFIG_PATH / 'config.ini', 'w') as configfile:
        config.write(configfile)
    logging.info(f'更新配置 - {option}: {new_value}')

# 配置日志
log_file = LOG_PATH / 'application.log'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=log_file,
                    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def array2QImage(image) -> QImage:
    height, width, channel = image.shape
    return QImage(image, width, height,  width * channel, QImage.Format_RGB888)

class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        # raise NotImplementedError
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.model = torch.hub.load(f"../", "yolov5s", source="local")
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.video = None
        self.bind_slots()

    def bind_slots(self) -> None:
        self.timer.timeout.connect(self.video_prediction)
        self.image_detect.clicked.connect(self.open_image)
        self.video_detect.clicked.connect(self.open_video)
        self.chenge_model.triggered.connect(self.chenge_model_)

    def chenge_model_(self) -> None:
        file_path = QFileDialog.getOpenFileNames(self,
                                                dir=config.get('Paths', 'ModelDir'),
                                                filter="*.pt")
        model_path, _ = file_path
        if model_path:
            model_path = model_path[0]
            self.new_method(model_path)
            logging.info(f"选择模型: {model_path}")
            self.model = torch.hub.load(f"../", "custom", path=model_path, source="local")
            logging.info(f"加载成功: {model_path.rsplit('/', 1)[-1]}")

    def new_method(self, model_path):
        update_config('Paths', 'ModelDir', model_path)

    def open_image(self) -> None:
        logging.info("点击了: 图片检测")
        file_path = QFileDialog.getOpenFileNames(self,
                                                dir=config.get('Paths', 'ImageDir'),
                                                filter="*.jpg;*.jpeg;*.png;*.bmp")
        image_path, _ = file_path
        logging.info(f"选择图片: {image_path}")
        if image_path:
            image_path = image_path[0]
            update_config('Paths', 'ImageDir', image_path.rsplit('/', 1)[0])
            self.input.setPixmap(QPixmap(image_path))
            logging.info(f"加载图片: {image_path.rsplit('/', 1)[-1]}")
            qimage = self.image_prediction(image_path)
            self.output.setPixmap(QPixmap.fromImage(qimage))
            logging.info(f"推理完成: {image_path.rsplit('/', 1)[-1]}")

    def image_prediction(self, image_path) -> QImage:
        results = self.model(image_path)
        image = results.render()[0]
        return array2QImage(image)

    def open_video(self) -> None:
        logging.info("点击了: 视频检测")
        file_path = QFileDialog.getOpenFileNames(self,
                                                dir=config.get('Paths', 'VideoDir'),
                                                filter="*.mp4;*.avi")
        video_path, _ = file_path
        logging.info(f"选择视频: {video_path}")
        if video_path:
            video_path = video_path[0]
            logging.info(f"加载视频: {video_path.rsplit('/', 1)[-1]}")
            update_config('Paths', 'VideoDir', video_path.rsplit('/', 1)[0])
            self.video = cv2.VideoCapture(video_path)
            self.timer.start()
            logging.info(f"开始推理视频: {video_path.rsplit('/', 1)[-1]}")




    def video_prediction(self) -> None:
        ret, frame = self.video.read()
        if not ret:
            self.timer.stop()
            print("推理结束")
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.input.setPixmap(QPixmap.fromImage(array2QImage(frame)))
            results = self.model(frame)
            qframe = results.render()[0]
            self.output.setPixmap(QPixmap.fromImage(array2QImage(qframe)))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()