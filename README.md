## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir submission
cd submission
pipenv install
pipenv shell
pip install -r requirements.txt
```
## Untuk menjalankan file .ipynb
setelah masuk ke venv silahkan masuk ke jupyter-notebook atau colab. disini saya memakai jupyter dengan perintah 
```
jupyter-notebook .
```
jangan lupa untuk masuk ke folder submission dahulu

## Run steamlit app
masuk ke IDE, disini saya menggunakan VSC dan jika sudah masuk ke VSC masuk ke folder:
```
cd dashboard
```

setelah itu jalankan dashboard dengan perintah
```
streamlit run dashboard.py
```
