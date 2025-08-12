from PIL import Image
import numpy as np
import os

def is_target_pattern(img_array, x, y):
    """检查是否为目标模式：边长为5，厚度为2的白色方框内含3x3黑色方块"""
    #print(f"检查是否为目标方框...坐标为{x, y}")
    #print(len(img_array))
    # 检查白色边框
    for i in range(5):
        # 上边框 (第1)

        if not (img_array[y, x+i] == 255 ):
            #print("第一行不对")
            return False
        # 下边框 (第5行)
        if not ( img_array[y+4, x+i] == 255):
            #print("第五行不对")
            return False
        # 左边框 (第1列)
        if not (img_array[y+i, x] == 255 ):
            #print("第一列不对")
            return False
        # 右边框 (第5列)
        if not (img_array[y+i, x+4] == 255):
            #print("第五 行不对")
            return False
    #print("检查白色完毕")
    # 检查内部3x3黑色区域
    for i in range(2, 5-2):
        for j in range(2, 5-2):
            if img_array[y+i, x+j] != 0:  # 不是黑色
                return False
    return True

def find_and_crop_patterns(image_path, output_prefix="pattern"):
    """查找并截取目标模式区域"""
    # 打开图片并转换为灰度图
    print("正在处理图片...")
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)
    height, width = img_array.shape
    white_count =0
    patterns = []
    for y in range(height - 5 + 1):
        for x in range(width - 5 + 1):
            # 找到第一个白色像素
            if img_array[y, x] == 255:
                #print("找到一个白色像素")
                white_count+=1
                if is_target_pattern(img_array, x, y):
                    patterns.append((x, y))
                    # 跳过这个区域，避免重复检测
                    x += 4
    print(white_count)
    # 截取并保存找到的模式区域
    #for i, (x, y) in enumerate(patterns):
       # # 截取5x5区域
        #cropped = img.crop((x, y, x+5, y+5))
        #cropped.save(f"{output_prefix}_{i+1}.png")
        #print(f"找到模式并保存: {output_prefix}_{i+1}.png")
    
    # 如果找到至少2个模式，截取它们之间的区域
    if len(patterns) >= 2:
        x1, y1 = patterns[0]
        x2, y2 = patterns[1]
        # 计算包含两个模式的矩形区域
        img_o = Image.open(image_path)
        left = min(x1, x2)
        top = min(y1, y2)
        right = max(x1+5, x2+5)
        bottom = max(y1+5, y2+5)
        region = img_o.crop((left, top, right, bottom))

        region = region.crop((5,5,region.width-5,region.height-5))
        region.save(f"{output_prefix}_region.png")
        print(f"保存两个模式之间的区域: {output_prefix}_region.png")
        return region

def Anti_source_by_data(path:str):
    input_image = path  # 替换为你的图片路径
    
    if not os.path.exists(input_image):
        print(f"错误: 输入图片 '{input_image}' 不存在")
    else:
        return find_and_crop_patterns(input_image)
if __name__ == "__main__":
    input_image = "测试图片.png"  # 替换为你的图片路径
    
    if not os.path.exists(input_image):
        print(f"错误: 输入图片 '{input_image}' 不存在")
    else:
        find_and_crop_patterns(input_image)