# ACNR-Automatic-Container-Number-Recognition-
ACNR merupakan sistem yang dapat melakukan detection dan recognition pada nomor box kendaraan kontainer. Sistem ini diciptakan dengan menggunakan YOLO v5 dan easyocr untuk ekstraksi teks dari gambar dan secara real time. 

**Program ini dibuat dengan menggunakan python version 3.8 pada operating system windows serta dijalankan pada jupyter notebook**

## Langkah Menjalankan Program
1. Buat folder baru

2. Clone repo ini : https://github.com/Yundapuji/ACNR-Automatic-Container-Number-Recognition-

3. Buat folder 'Model' di dalam folder 2. Prediction

4. Di dalam folder Model download folder weights : https://drive.google.com/drive/folders/1-ch3crLhyg2mKRWh7zl17bUHvE-IvV_z?usp=sharing 

5. Membuat virtual environment dan activate environment tersebut
    - Masuk di path folder yang telah dibuat
    - ```pip install vitualenv ```
    - Buka powershell di cmd 
    - ```virtualenv -p 'path dari python.exe yang akan digunakan' nama_virtual_environment```
    - Keluar dari powershell 
    - Activate virtual environment
      ```.\nama_virtual_environment\Scripts\activate```
      
6. Download dependensi yang di perlukan dan menambahkan virtual environment di python kernel jupyter notebook
    - ```pip install -r requirements.txt```
    - ```python -m ipykernel install --user --name=nama_virtual_environment```
    
7. Masuk di path folder 2. Prediction ```cd 2. Prediction``` dan membuka jupyter notebook
    - ```jupyter notebook```

8. Buka Notebook [00. Predictions.ipynb]("./2. Prediction/00. Predictions.ipynb")

10. Untuk file input yang akan dideteksi dapat dipilih pada folder [TestModel](URL "tooltip")
     



