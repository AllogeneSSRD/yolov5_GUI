"""
去除数字中的其他字符, 修改图片路径, 优化识别率
"""
import csv
import os

from datetime import datetime
from pathlib import Path

import torch
import pytesseract
import cv2
import numpy as np

from PIL import Image, ImageDraw, ImageOps, ImageFilter
from PIL import ImageFont


# 应用根目录
BASE_PATH = Path(__file__).parent.resolve()

# 加载素材识别模型
model = torch.hub.load("", 'custom', path=f"{BASE_PATH}\\SR.pt", source="local")  # 确保路径正确

# 指定中文字体的路径
font_path = f"{BASE_PATH}\\font\\LXGWWenKai-Bold.ttf"
# 设置字体和大小
font = ImageFont.truetype(font_path, size=20)
font_prep = ImageFont.truetype(font_path, size=36)

synthesis_material = {
    "prosperity_certificate": "商业活力证明",
    "mechanical_cube": "机械立方",
    "weary": "厌倦",
    "mythus_knots": "迷思绳结",
    "tear_crystal_of_glorious_death": "哀荣泣石",
    "phase_flame": "相位灵火",
    "interdimensional_leaf": "换境树叶",
    "thermal_gel": "散热凝胶",
    "the_sound_and_the_fury": "喧哗与骚动",
    "dragon_scale_coral": "龙鳞珊瑚",
    "slime_of_harmony": "同谐黏液",
    "Tree_bark_of_erudition": "智识树皮",
    "hard_chip_of_nihility": "虚无硬片",
    "Preservation Construction Material": "存护筑材",
    "Stone of The Hunt": "巡猎石",
    "Ambergris of Abundance": "丰饶香涎",
    "Strange Matter of Destruction": "毁灭异质",
    "Old Molar": "老旧臼齿",
    "Hunger": "饥饿",
    "Confounding": "迷茫",
    "Tian Dong": "鳞渊天冬",
    "Extract of Medicinal Herbs": "药草提取物",
    "Jade Abacus Unit": "玉兆单元",
    "Meteoric Alloy": "陨铁",
    "Leaf of Imaginary": "虚数残叶",
    "Quantum Ripples": "量子涟漪",
    "Vortex of Wind": "风之旋",
    "Eye of Lightning": "雷之眼",
    "Core of Ice": "冰之芯",
    "Feather of Flame": "火之翎",
    "Protein Rice": "蛋白米",
    "Virtual Particle": "虚粒子",
    "Mechanical Parts": "零件",
    "Rusty Gear": "锈迹齿轮",
    "Broken Dreams": "碎梦",
    "Tranquility": "安逸",
    "Human-Height Auspicious Crops": "一人嘉禾",
    "Discarded Ingenium Parts": "废弃机巧零件",
    "Seed": "种子",
    "Gaseous Liquid": "气态流体",
    "Metal": "金属",
    "Phlogiston": "燃素",
    "Basic Ingredients": "基本食材",
    "Solid Water": "固态净水",
    }

def preprocess_image(image_path, preprocessed_image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    size = 2
    img = cv2.resize(img, (img.shape[1] * size, img.shape[0] * size), interpolation=cv2.INTER_LINEAR)

    # 应用轻微的图像增强
    img = cv2.equalizeHist(img)

    # 二值化 - 需要根据图像内容调整阈值
    _, img = cv2.threshold(img, 185, 255, cv2.THRESH_BINARY)

    kernel_size = 3  # 结构元素的大小
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # 腐蚀
    img = cv2.erode(img, kernel, iterations=1)

    # 膨胀
    img = cv2.dilate(img, kernel, iterations=1)

    cv2.imwrite(preprocessed_image_path, img)

    img = Image.fromarray(img)
    return img

def detect_and_annotate(image_path, preprocessed_image_path, model, output_path):
    img = Image.open(image_path)
    numimg = Image.open(preprocessed_image_path)

    results = model(img)
    detected_objects = results.xyxy[0]
    draw = ImageDraw.Draw(img)
    draw_prep = ImageDraw.Draw(numimg)

    materials_count = {key: [] for key in synthesis_material}

    for obj in detected_objects:
        obj = obj.tolist()

        xmin, ymin, xmax, ymax = obj[:4]

        num_ymin = int(ymax - 5)  # 稍微在素材下边框的上面开始
        num_ymax = int(num_ymin + 30)  # 假设数字的高度不会超过30像素
        num_xmin = int(xmin + 20)
        num_xmax = int(xmax - 20)

        size = 2

        num_region = numimg.crop((int(size * num_xmin), int(size * num_ymin), int(size * num_xmax), int(size * num_ymax)))

        # 使用OCR技术来识别数字
        number = pytesseract.image_to_string(num_region, config='--psm 8 digits')
        number = number.replace("-", " ").replace(".", " ")

        draw.rectangle([(num_xmin, num_ymin), (num_xmax, num_ymax)], outline="blue", width=2)
        draw_prep.rectangle([(int(size * num_xmin), int(size * num_ymin)), (int(size * num_xmax), int(size * num_ymax))], outline="white", width=4)

        draw.text((xmin + 14, num_ymax - 12), number.strip(), fill="white", font=font)
        draw_prep.text((int(size * xmin + 14), int(size * num_ymax - 12)), number.strip(), fill="white", font=font_prep)

        class_id = int(obj[5])
        class_name = model.names[class_id]
        chinese_name = synthesis_material.get(class_name, class_name)  # 获取中文名称，如果不存在则使用原名
        print(f'素材 {chinese_name:<10}数量: {number.strip()}')

        if not materials_count[class_name]:
            materials_count[class_name] = [chinese_name, number.strip()]

        draw.rectangle([(xmin, ymin), (xmax, ymax)], outline="red", width=2)
        draw.text((xmin + 5, ymin + 5), chinese_name, fill="red", font=font)

    img.save(output_path)
    numimg.save(preprocessed_image_path)
    img.show()

    return materials_count

def save_to_csv(materials_count, csv_path):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    filename_time = datetime.now().strftime(' %Y-%m-%d %H-%M-%S')
    base_name, extension = os.path.splitext(csv_path)
    new_filename = base_name + filename_time + extension
    new_file_path = os.path.join(BASE_PATH, new_filename)
    # print(new_file_path)
    with open(new_file_path, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow([current_time])
        for key, value in materials_count.items():
            writer.writerow([key] + value)

if __name__ == "__main__":
    image_path = f"{BASE_PATH}\\sample.png"                """这里填写需要检测的图片路径"""
    preprocessed_image_path = f"{BASE_PATH}\\preprocessed_image.png"
    annotated_image_path = f"{BASE_PATH}\\annotated_image.png"
    csv_path = f"{BASE_PATH}\\合成素材.csv"
    preprocess_image(image_path, preprocessed_image_path)
    materials_count = detect_and_annotate(image_path, preprocessed_image_path, model, annotated_image_path)
    save_to_csv(materials_count, csv_path)