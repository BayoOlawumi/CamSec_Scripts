import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

under_watch = '/Users/BayoOlawumi/Downloads'
video_fmt = [".mp4",".avi",".flv",".mpg4",".webm"]
picture_fmt = [".jpg",".png", ".gif",".jpeg"]
docs_fmt = [".docx",".pdf",".txt",]
audio_fmt = [".mp3",".wav",".m4a"]
set_up_fmt = [".exe"]

class MyFileHandler(FileSystemEventHandler):
    
    def on_modified(self, event):
        print("Okay")
        for each_file in os.listdir(under_watch):
            print(each_file)
            each_file_path = os.path.join(under_watch,each_file)
            if os.path.isfile(each_file_path):
                print(each_file)
                file_type = os.path.splitext(each_file_path)[-1].lower()
                # Check categories
                #-----Videos
                if str(file_type) in video_fmt:
                    shutil.move(each_file_path, os.path.join(under_watch,"/Video"+each_file))
                    print("Video ni oo")
                #------Audio
                elif str(file_type) in audio_fmt:
                    shutil.move(each_file_path, os.path.join(under_watch,"/Audio"+each_file))
                    print("Audio ni oo")
                #------Picture
                elif str(file_type) in picture_fmt:
                    shutil.move(each_file_path, os.path.join(under_watch,"/Picture"+each_file))
                    print("Picture ni oo")
                #------Documents
                elif str(file_type) in docs_fmt:
                    shutil.move(each_file_path, os.path.join(under_watch,"/Documents"+each_file))
                    print("Document ni oo")
                #------Set Up
                elif str(file_type) in set_up_fmt:
                    shutil.move(each_file_path, os.path.join(under_watch,"/Programs"+each_file))
                    print("Programs ni oo")
                #------Others  
                else:
                    shutil.move(each_file_path, os.path.join(under_watch,"/Compressed"+each_file))
                    print("Compressed ni oo")



my_handler = MyFileHandler()
observer = Observer()
observer.schedule(my_handler, under_watch, recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()

observer.join()
