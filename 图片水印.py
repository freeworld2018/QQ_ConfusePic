from PIL import Image, ImageDraw

def add_border_and_markers(input_path, output_path):
    # 打开原始图片
    original_img = Image.open(input_path)
    
    # 创建带黑色描边的新图片（原图每边扩展10像素）
    bordered_img = Image.new('RGB', 
                           (original_img.width + 20, original_img.height + 20),
                           color='black')
    bordered_img.paste(original_img, (10, 10))
    
    # 创建绘图对象
    draw = ImageDraw.Draw(bordered_img)
    
    # 左上角白色方框（5×5像素，1像素厚度）
    left_top_box = [
        (10 - 5, 10 - 5),           # 左上角（向内偏移1像素）
        (9 , 9)            # 右下角
    ]
    draw.rectangle(left_top_box, outline='white', width=1)
    
    # 右下角白色方框（5×5像素，1像素厚度）
    right_bottom_box = [
        (10 + original_img.width , 10 + original_img.height),  # 左上角
        (10 + original_img.width + 4, 10 + original_img.height + 4)           # 右下角
    ]
    draw.rectangle(right_bottom_box, outline='white', width=1)
    
    # 保存结果
    bordered_img.save(output_path)
    print(f"处理完成，结果已保存到: {output_path}")

# 使用示例
#input_image = "test_mark_pic.jpg"  # 输入图片路径
#output_image = "output.jpg"  # 输出图片路径
#add_border_and_markers(input_image, output_image)