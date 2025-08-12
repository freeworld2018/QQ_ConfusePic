import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import 逆图片混淆 as anti_pic
import 图片混淆 as defuse_pic
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:  # 只监听文件，忽略文件夹
            print(f"新文件创建: {event.src_path}")
            if event.src_path.endswith(".png"):  # 只监听png文件
                data_cliped = anti_pic.Anti_source_by_data(event.src_path)
            else:
                data_cliped = None
            if data_cliped:
                print("检测到混淆图片")
                time.sleep(1)
                print("等待占用结束")
                data_cliped.save("temp_pic.png","png")
                defuse_pic.anti_confuse_image("temp_pic.png",event.src_path,16)
                print("完成图片修改")
            else:
                print("未检测到混淆图片")
            

if __name__ == "__main__":
    folder_to_watch = "C:/Users/xutianci/Documents/Tencent Files/971308078/nt_qq/nt_data/Pic/2025-08/Ori"  # 要监听的文件夹路径
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()  # 启动监听
    print("开始监听文件...")
    try:
        while True:
            time.sleep(1)  # 保持主线程运行
    except KeyboardInterrupt:
        observer.stop()  # 按 Ctrl+C 停止监听
    observer.join()