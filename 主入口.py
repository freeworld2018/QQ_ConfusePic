import threading
import tkinter as tk
from PIL import ImageGrab, ImageTk
from PIL import Image
from pynput import keyboard, mouse
import win32clipboard
from io import BytesIO
import 逆图片混淆 as anti_pic
import 图片混淆 as defuse_pic
import 图片水印 as mark_pic

class ScreenshotTool:
    def __init__(self):
        self.screenshot = None
        self.start_point = None
        self.end_point = None
        self.is_selecting = False
        self.root = None  # tkinter根窗口
        self.canvas = None  # 用于显示图像的画布
        self.tk_image = None  # 保持对图像的引用
        self.listen_thread = None

        # 设置热键监听
        self.hotkey_listener = keyboard.GlobalHotKeys({
            '<ctrl>+t': self.start_screenshot
        })
        self.hotkey_listener.start()
        
        # 鼠标监听
        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click
        )
        self.mouse_listener.start()
        
    def start_screenshot(self):
        """开始截图流程"""
        print("开始截图，请拖动鼠标选择区域 (ESC取消)")
        self.screenshot = ImageGrab.grab()
        self.is_selecting = True
        self.start_point = None
        self.end_point = None
        
        # 显示抓取的屏幕内容
        if self.root:

            self.root.after(0,self.show_screenshot)
        #self.show_screenshot()     
        self.gui_thread = threading.Thread(target=self.show_screenshot, daemon=True)
        self.gui_thread.start()
        
    def show_screenshot(self):
        """显示抓取的屏幕内容"""
        """使用tkinter显示屏幕截图"""
        if not self.root:
        #    self.root.destroy()  # 关闭之前的窗口
             
            self.root = tk.Tk()
            self.root.attributes('-fullscreen', True)  # 全屏显示
            self.root.attributes('-topmost', True)  # 置顶窗口
            self.root.attributes('-alpha', 1.0)  # 设置透明度
        else:
            self.root.deiconify()
            self.root.lift()



        if self.canvas:
            self.canvas.destroy()
            
        # 创建新的画布并显示图像
        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 更新图像
        self.tk_image = ImageTk.PhotoImage(self.screenshot)
        self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)
        
        # 绑定ESC键
        self.root.bind('<Escape>', lambda e: self.cleanup())
        
        # 显示窗口
        #self.root.mainloop()
        
    def on_move(self, x, y):
        """鼠标移动事件"""
        #print(f"鼠标移动到: {x}, {y}")
        if self.is_selecting and self.start_point and self.canvas:
            self.end_point = (x, y)
            self.update_selection_display()
            
    def on_click(self, x, y, button, pressed):
        #print(f"鼠标点击: {x}, {y}")
        """鼠标点击事件"""
        if not self.is_selecting:
            return
            
        if pressed and button == mouse.Button.left:
            self.start_point = (x, y)
            print(f"开始选择: {self.start_point}")
        elif not pressed and button == mouse.Button.left and self.start_point:
            self.finish_selection()
            
    def update_selection_display(self):
        """更新选择区域的显示"""
        if not self.start_point or not self.end_point or not self.canvas:
            return
            
        # 清除之前的矩形
        self.canvas.delete("selection")
        
        # 计算选择区域
        x1, y1 = self.start_point
        x2, y2 = self.end_point
        
        # 绘制红色边框
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline="red", width=2,
            tags="selection"
        )
        
    def finish_selection(self):
        print("开始执行完成部分")
        """完成选择并复制到剪贴板"""
        if not self.start_point or not self.end_point:
            return
            
        x1, y1 = self.start_point
        x2, y2 = self.end_point
        
        # 确保x1,y1是左上角，x2,y2是右下角
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
            
        # 裁剪图像
        cropped = self.screenshot.crop((x1, y1, x2, y2))
        
        # 复制到剪贴板
        cropped.save("clipboard.png", "png")
        #上面是保存到本地，下面事保存到剪贴板
        



        output = BytesIO()
        cropped.convert('RGB').save(output, 'BMP')
        data = output.getvalue()
        output.close()
        
        data_cliped = anti_pic.Anti_source_by_data("clipboard.png")


        
        if data_cliped:
            print("检测到有效图片")
            #data_cliped.save("temp_pic.bmp")
            data_cliped.save("temp_pic.png","png")
            defuse_pic.anti_confuse_image("temp_pic.png","temp_pic_defuse.png",16)
            print("解密成功,文件名为“temp_pic_defuse.png")
            image_theading = threading.Thread(target = show_png)
            image_theading.start()
            #Image.open("temp_pic_defuse.png").show()
            out_put_1 = BytesIO()
            data_cliped.convert('RGB').save(out_put_1, 'BMP')
            data_clip = out_put_1.getvalue()
            out_put_1.close()
        else:
            print("没有检测到有效图片")
            #data_cliped.save("temp_pic.bmp")
            defuse_pic.confuse_image("clipboard.png","confuse_temp_pic.png",16)
            mark_pic.add_border_and_markers("confuse_temp_pic.png","mark_pic.png")
            data_clip = None


        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        if data_clip:
            print("检测到有效图片")
            #defuse_pic.anti_confuse_image("mark_pic.png","temp_pic.png")
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data_clip[14:])  # 跳过BMP文件头
        else:
            print("没有检测到有效图片")
            #defuse_pic.confuse_image()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data[14:])
        win32clipboard.CloseClipboard()
        self.cleanup()

        
    def cleanup(self):
        print("清理资源")
        """清理资源"""
        self.is_selecting = False
        if self.root:
            self.root.withdraw()
            #self.root.iconify()
            #self.root.destroy()
            #self.root = None
        if self.screenshot:
            self.screenshot.close()
            self.screenshot = None
        self.start_point = None
        self.end_point = None
        
    def run(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)  # 全屏显示
        self.root.attributes('-topmost', True)  # 置顶窗口
        self.root.attributes('-alpha', 1.0)  # 设置透明度
        self.root.withdraw()
        self.root.mainloop()
        self.listen_thread = threading.Thread(target=self.listen_to, daemon=True)
        """运行主循环"""
    def listen_to(self):
        try:
            # 监听ESC键
            with keyboard.Listener(on_press=self.on_key_press) as key_listener:
                key_listener.join()
        except KeyboardInterrupt:
            self.cleanup()
            
    def on_key_press(self, key):
        """键盘事件 - ESC取消"""
        if key == keyboard.Key.esc and self.is_selecting:
            print("截图已取消")
            self.cleanup()

def show_png():
    Image.open("temp_pic_defuse.png").show()


if __name__ == "__main__":
    tool = ScreenshotTool()
    print("截图工具已启动，按Ctrl+T开始截图...")
    tool.run()

    