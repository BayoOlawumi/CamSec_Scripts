from connectivity_checker import connect
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import boto3
import pandas as pd
from datetime import datetime, timedelta
import pytz
import glob
import os
import time


s3_client = boto3.client('s3')
dumps = "/Users/HP/Desktop/monitor_me/overdue"
vid_folder = "/Users/HP/Desktop/monitor_me"
tz_NG = pytz.timezone('Africa/Lagos')
video_fmt = [".mp4",".avi",".flv",".mpg4",".webm",".3gp"]
upload_status = " "
threshold_days= 0
over_threshold_days = 10
dumping_folder ='overdue'
target_folder = glob.glob(vid_folder+'/*')



def upload_files(file_name, bucket_name, object_name, date_created, date_sent):

    if object_name is None:
        object_name = file_name
    # Main File Uploader
    response = s3_client.upload_file(file_name, bucket_name, object_name, ExtraArgs = {
        'ACL': 'public-read',
        'Metadata':{
            'creation date': date_created,
            'time-sent': date_sent,
        }})
    upload_status = "File Uploaded Successfully"
    print_me(upload_status)



def display_days_spent(present_time, each_file_path):
    # Get the date each file was created
    created_date = datetime.fromtimestamp(os.path.getctime(each_file_path))
    # Evaluate the differences
    days_spent_on_pc = (present_time - created_date).days
    return days_spent_on_pc
        


def load_server():
    for each_file in target_folder:
            time_sent = datetime.now(tz_NG).strftime("%d/%m/%y")
            time_created = (datetime.now(tz_NG) - timedelta(days=20)). strftime("%d/%m/%y")
            # Check File File format, ensure it is in video format
            while os.path.isfile(each_file) and os.path.splitext(each_file)[-1].lower() in video_fmt:
                upload_files(each_file,'camsec-futa',each_file+str(time_sent),time_created, time_sent)
                upload_status = "uploading to the server"
                print_me(upload_status)
                print(each_file.rjust(60,"#"))

def print_me(text):
    print(text.center(100,"*"))



class TheHandler(FileSystemEventHandler):
    file_name = " "
    def on_created(self, event):
        print("God Rules")
        #self.clean_home()
        #load_server()

    def on_modified(self, event):
        #print("God Rules")
        self.clean_home()
        load_server()
        pass



    def clean_home(self): 
        # Iterate through every file in the given folder to monitor
        present_time = datetime.now()
        for each_file in os.listdir(vid_folder):
            # Join file name to path
            each_file_path = vid_folder + "/" + each_file            
            # Check if each file is a file but not folder and also not a shortcut
            if os.path.isfile(each_file_path):
                days_spent_on_pc = display_days_spent(present_time, each_file_path)
                # Only extract those whose days are more than threshold
                self.move_longstayed_files(each_file, days_spent_on_pc)
                if days_spent_on_pc > threshold_days:
                    try:
                        self.move_longstayed_files(each_file, days_spent_on_pc)
                        transfer_status = "{0} transferred successfully".format(each_file)
                    except:
                        transfer_status = "Error transferring {0}".format(each_file_path)
                    print_me(transfer_status)

                elif days_spent_on_pc > over_threshold_days:
                    try:
                        os.remove(each_file_path)
                        delete_status = "{0} deleted successfully".format(each_file_path)
                    except:
                        delete_status = "Error transferring {0}".format(each_file_path)
                    print_me(delete_status)
            # In a case where the content is not a file 
            elif os.path.isdir(each_file_path):
                    days_spent_on_pc = display_days_spent(present_time, each_file_path)
                    folder_name = each_file_path.split("/")[-1]
                    # Only extract those whose days are more than threshold
                    while folder_name != "overdue":
                        if days_spent_on_pc > threshold_days:
                            try:
                                self.move_longstayed_files(each_file, days_spent_on_pc)
                                transfer_status = "{0} transferred successfully".format(each_file_path)
                            except:
                                transfer_status = "Error transferring {0}".format(each_file_path)
                            print_me(transfer_status)
                        # Delete 
                        elif days_spent_on_pc > over_threshold_days:
                            try:
                                shutil.rmtree(each_file_path)
                                delete_status = "{0} deleted successfully".format(each_file_path)
                            except:
                                delete_status = "Error transferring {0}".format(each_file_path)
                            
                            print_me(delete_status)



    def move_longstayed_files(self, each_file, expended_days):
        # Ensure the folder gabbage is not being put in itself
        print_me("clean home")
        if each_file != dumping_folder:
            # check if the file path already exist
            incoming_file_path = vid_folder + '/' + each_file
            if os.path.isfile(incoming_file_path):
                new_name = each_file
                i = 1
                # Incase there are many of these duplicate files in the Gabbage folder already
                while incoming_file_path:
                    i += 1
                    new_name = os.path.splitext(vid_folder + '/'+ new_name)[0] + str(i) + os.path.splitext(incoming_file_path)[-1]
                    new_name = new_name.split("/")[5]
                    incoming_file_path = os.path.isfile(vid_folder +"/" + new_name)

                # Real file transfer going on here
                old_path = vid_folder + "/" + each_file
                new_path = dumps + "/" + new_name
                os.rename(old_path, new_path)
                upload_status = new_name + " was successfully moved to "+ dumping_folder +" folder after spending "+ str(expended_days) + " days!"
                print_me(upload_status)


handler = TheHandler()
observer = Observer()
observer.schedule(handler,vid_folder,recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()

observer.join()

