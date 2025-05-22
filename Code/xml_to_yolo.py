import os
import xml.etree.ElementTree as ET
from pathlib import Path

class_map = {"wildfire": 0}  # 单类别映射


def convert_voc_to_yolo(xml_path, output_dir):
    """处理单个XML文件转换，自动处理空文件和异常"""
    xml_path = Path(xml_path)
    output_path = Path(output_dir) / f"{xml_path.stem}.txt"

    # 处理空文件
    if xml_path.stat().st_size == 0:
        output_path.write_text("")  # 创建空txt
        return

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 获取图像尺寸（带默认值）
        size = root.find("size")
        try:
            img_w = float(size.find("width").text)
            img_h = float(size.find("height").text)
        except (AttributeError, TypeError):
            print(f"警告: {xml_path} 尺寸异常，使用默认640x640")
            img_w, img_h = 640, 640

        # 处理标注对象
        yolo_lines = []
        for obj in root.iter("object"):
            try:
                cls_name = obj.find("name").text
                class_id = class_map[cls_name]
                bbox = obj.find("bndbox")

                # 坐标转换
                x_center = (float(bbox.find("xmin").text) + float(bbox.find("xmax").text)) / 2 / img_w
                y_center = (float(bbox.find("ymin").text) + float(bbox.find("ymax").text)) / 2 / img_h
                width = (float(bbox.find("xmax").text) - float(bbox.find("xmin").text)) / img_w
                height = (float(bbox.find("ymax").text) - float(bbox.find("ymin").text)) / img_h

                yolo_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
            except Exception as e:
                print(f"跳过 {xml_path} 中的无效标注: {str(e)}")
                continue

        # 写入文件
        output_path.write_text("\n".join(yolo_lines))

    except Exception as e:
        print(f"转换失败: {xml_path} - {str(e)}")
        if not output_path.exists():
            output_path.write_text("")  # 创建空文件保证后续流程


# 批量处理
for split in ["train", "val"]:
    input_dir = Path(f"yolov5/DataSet/labels/{split}")
    output_dir = Path(f"yolov5/DataSet/labels/{split}_yolo")

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"正在转换 {input_dir}...")
    for xml_file in input_dir.glob("*.xml"):
        convert_voc_to_yolo(xml_file, output_dir)

    print(f"完成: {input_dir} → {output_dir}")
    print(f"生成文件数: {len(list(output_dir.glob('*.txt')))}")