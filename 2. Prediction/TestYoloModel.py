#Import Library
import cv2
import numpy as np
import os
import yaml
import easyocr
from yaml.loader import SafeLoader

class yolo_pred():
    def __init__(self,onnx_model,data_yaml):
        # ### Load Yaml
        with open('Data.yaml',mode = 'r') as f:
            data_yaml = yaml.load(f,Loader = SafeLoader) #Apakah pake .self juga?

        self.labels = data_yaml['names']
        self.nc = data_yaml['nc']
        
        # ### Load YOLO Model
        self.yolo = cv2.dnn.readNetFromONNX('./Model/weights/best.onnx')
        self.yolo.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.yolo.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    
    def extract_text(self, image, bbox):
        x, y, w, h = bbox
        cropped_image = image[y:y+h, x:x+w]
        reader = easyocr.Reader(['id']) 
        result = reader.readtext(cropped_image)
        text = ' '.join([res[1] for res in result])
        return text
    
    def predictions(self,image):
        row, col, d = image.shape

        # ### Menerapkan YOLO Prediction Dari Gambar Test Akhir
        #----1. Convert gambar ke square matriks
        max_rc = max(row,col)
        input_image = np.zeros((max_rc,max_rc,3),dtype=np.uint8)
        input_image[0:row, 0:col] = image

        #----2. Mendapatkan prediksi dari square array/square matriks
        INPUT_WH_YOLO = 640
        blob = cv2.dnn.blobFromImage(input_image,1/255,(INPUT_WH_YOLO,INPUT_WH_YOLO),swapRB = True, crop = False)
        self.yolo.setInput(blob)
        preds = self.yolo.forward() #Deteksi/Prediksi dari YOLO

        # ### Non Maximum Supression
        #----1. Filter deteksi berdasarkan nilai confidence (0.4) dan probability score (0.25)
        detections = preds[0]
        boxes = []
        confidences = []
        classes = []

        #Width dan height dari gambar (input_image)
        image_w, image_h = input_image.shape[:2]
        x_factor = image_w/INPUT_WH_YOLO
        y_factor = image_h/INPUT_WH_YOLO

        for i in range(len(detections)):
            row = detections[i]
            confidence = row[4] #Confidences dari hasil deteksi objek
            if confidence > 0.4:
                class_score = row[5:].max() #Maximum probability dari 5 objek
                class_id = row[5:].argmax() #Mendapatkan posisi index saat max probability muncul

                if class_score > 0.25:
                    cx, cy, w, h = row[0:4]

                    #Membuat Bounding Box dari value yang sudah didapatkan
                    #Left, Top, Width, Height
                    left = int((cx - 0.5*w)*x_factor)
                    top = int((cy - 0.5*h)*y_factor)
                    width = int(w*x_factor)
                    height = int(h*y_factor)

                    box = np.array([left, top, width, height])

                    #Append value dalam list kosong yang telah dibuat
                    confidences.append(confidence)
                    boxes.append(box)
                    classes.append(class_id)

        #Cleaning duplikat value
        boxes_np = np.array(boxes).tolist()
        confidences_np = np.array(confidences).tolist()

        #NMS (Non Maximum Supression)
        index = np.array(cv2.dnn.NMSBoxes(boxes_np, confidences_np, 0.25, 0.45)).flatten()

        # ### Membuat Bounding Box Pada Gambar Test Akhir
        for ind in index:
            #Ekstrak Bounding Box
            x,y,w,h = boxes_np[ind]
            bb_conf = int(confidences_np[ind]+100) #Perlu evaluasi
            classes_id = classes[ind]
            class_name = self.labels[classes_id]
            colors = self.generate_colors(classes_id)

            text = f'{class_name}' ###########********
            
            # Ekstraksi teks
            bbox = (x, y, w, h)
            extracted_text = self.extract_text(image, bbox)

            cv2.rectangle(image, (x-10, y-10), (x+w+10, y+h+10), colors, 2)
            cv2.rectangle(image, (x-10, y-40), (x+w+10, y), colors, -1)
            cv2.putText(image, text, (x,y-10), cv2.FONT_HERSHEY_PLAIN, 0.7, (0,0,0), 1)
            cv2.putText(image, extracted_text, (x, y + h + 20), cv2.FONT_HERSHEY_PLAIN, 2.1, (255, 255, 0), 3)
        return image
    
    def generate_colors(self,ID):
        np.random.seed(10)
        colors = np.random.randint(100,255,size = (self.nc,3)).tolist()
        return tuple(colors[ID])
    
    

        