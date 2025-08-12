from PIL import Image

import numpy as np

def confuse_image(image_path, output_path,confuse_num:int):
    if confuse_num % 2 == 1:
        cols += 1 
    # 打开原图片
    img = Image.open(image_path)
    print("原始图片尺寸为"+str(img.size))
    crop_width = img.width % confuse_num
    crop_height = img.height % confuse_num
    
    img = img.crop((0,0,img.width-crop_width,img.height-crop_height))
    #print("裁剪后图片尺寸为"+str(img.size))")
    print("裁剪后图片尺寸为"+str(img.size))
    img_array = np.array(img)
    # 获取图片尺寸
    height, width = img_array.shape[0], img_array.shape[1]
    
    # 1. 先按行切割并交换
    # 计算每行的高度（8行）
    row_height = height // confuse_num
    rows = [img_array[i*row_height:(i+1)*row_height] for i in range(confuse_num)]
    
    # 交换行：1<->2, 3<->4, 5<->6, 7<->8
    for i in range(0, confuse_num, 2):
        if i+1 < confuse_num:  # 确保不越界
            rows[i], rows[i+1] = rows[i+1], rows[i]
    
    # 重新组合行
    row_confused = np.vstack(rows)
    
    # 2. 再按列切割并交换
    # 计算每列的宽度（8列）
    col_width = width // confuse_num
    # 注意：转置行列以便按列切割
    col_confused_transposed = row_confused.transpose(1, 0, 2)
    cols = [ col_confused_transposed[i*col_width:(i+1)*col_width] for i in range(confuse_num)]
    
    # 交换列：1<->2, 3<->4, 5<->6, 7<->8
    for i in range(0, confuse_num, 2):
        if i+1 < confuse_num:  # 确保不越界
            cols[i], cols[i+1] = cols[i+1], cols[i]
    
    # 重新组合列并转置回来
    col_confused = np.vstack(cols).transpose(1, 0, 2)
    

    row_height_2 = height // 4
    rows_2 = [col_confused[i*row_height_2:(i+1)*row_height_2] for i in range(4)]
    
    # 交换行：1<->2, 3<->4, 5<->6, 7<->8
    for i in range(0, 4, 2):
        if i+1 < confuse_num:  # 确保不越界
            rows_2[i], rows_2[i+1] = rows_2[i+1], rows_2[i]
    
    # 重新组合行
    row_confused_2 = np.vstack(rows_2)



    # 保存结果
    result_img = Image.fromarray(row_confused_2)
    result_img.save(output_path)
    print(f"图片已混淆并保存到: {output_path}")


def anti_confuse_image(image_path, output_path,confuse_num:int):
    if confuse_num % 2 == 1:
        cols += 1 
    # 打开原图片
    img = Image.open(image_path)
    img_array = np.array(img)
    
    # 获取图片尺寸
    height, width = img_array.shape[0], img_array.shape[1]
    
    row_height_2 = height // 4
    rows_2 = [img_array[i*row_height_2:(i+1)*row_height_2] for i in range(4)]
    
    # 交换行：1<->2, 3<->4, 5<->6, 7<->8
    for i in range(0, 4, 2):
        if i+1 < confuse_num:  # 确保不越界
            rows_2[i], rows_2[i+1] = rows_2[i+1], rows_2[i]
    
    # 重新组合行
    row_confused_2 = np.vstack(rows_2)

    # 2. 再按列切割并交换
    # 计算每列的宽度（8列）
    
    col_width = width // confuse_num
    
    # 注意：转置行列以便按列切割
    col_confused_transposed = row_confused_2.transpose(1, 0, 2)
    cols = [ col_confused_transposed[i*col_width:(i+1)*col_width] for i in range(confuse_num)]
    
    # 交换列：1<->2, 3<->4, 5<->6, 7<->8
    for i in range(0, confuse_num, 2):
        if i+1 < confuse_num:  # 确保不越界
            cols[i], cols[i+1] = cols[i+1], cols[i]
    
    # 重新组合列并转置回来
    col_confused = np.vstack(cols).transpose(1, 0, 2)










    # 1. 先按行切割并交换
    # 计算每行的高度（8行）
    row_height = height // confuse_num
    rows = [col_confused[i*row_height:(i+1)*row_height] for i in range(confuse_num)]
    
    # 交换行：1<->2, 3<->4, 5<->6, 7<->8
    for i in range(0, confuse_num, 2):
        if i+1 < confuse_num:  # 确保不越界
            rows[i], rows[i+1] = rows[i+1], rows[i]
    
    # 重新组合行
    row_confused = np.vstack(rows)
    

    




    # 保存结果
    result_img = Image.fromarray(row_confused)
    result_img.save(output_path)
    print(f"图片已混淆并保存到: {output_path}")


# 使用示例
#confuse_image("target_pic.jpg", "confused_pic.jpg",16)
#anti_confuse_image("target_pic.jpg", "confused_pic.jpg",16)