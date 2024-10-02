import cv2
from pyzbar.pyzbar import decode
from threading import Thread
import time
import numpy as np

myrtmp_addr = "http://192.168.1.60:8081/live/.m3u8"

class VideoStream:
    def __init__(self):
        print("init")
        self.stream = cv2.VideoCapture(myrtmp_addr)
        
        fps = self.stream.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 30.0
        self.frame_duration = 1.0 / fps
        
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        time.sleep(2.0)
    
    def start(self):
        print("start thread")
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self
    
    def update(self):
        print("read")
        sync = 0
        sync_time = time.time()

        while True:
            if self.stopped:
                return
            
            start_time = time.time()
            (self.grabbed, self.frame) = self.stream.read()

            sleep_time = max(0, self.frame_duration - (time.time() - start_time))

            
            if time.time() - sync_time > 10 and sync > 100:
                # deve ficar 5 segundos em sincronia
                

                print("sync_time")
                sync = 0
                sync_time = time.time() 
            if sync < 100:
                sync += 1
                print("sync:", sync)
                time.sleep(sleep_time)
                

            # print("frame_duration:", self.frame_duration)
            # print("sleep_time:", sleep_time)
            # print("duration:", (time.time() - start_time))
                
            
    def read(self):
        return self.frame
    
    def read_qr(self):
        qr_codes = decode(self.frame)
        self.frame_qr_code_data = []
        
        for qr_code in qr_codes:
            (x, y, w, h) = qr_code.rect
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            qr_data = qr_code.data.decode('utf-8')
            cv2.putText(self.frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            
            if qr_data not in self.frame_qr_code_data:
                self.frame_qr_code_data.append(qr_data)
            
        return self.frame

    
    def stop(self):
        self.stopped = True
