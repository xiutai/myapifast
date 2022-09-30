安装依赖：
pip install -r /绝对路径/requirements.txt

启动fastapi：
gunicorn main:app -b 0.0.0.0:8000 -w 2 --threads 2 -t 0 -k uvicorn.workers.UvicornH11Worker"# myapifast" 


uvicorn main:app --host='shop-ee.tw' --port='8001' --reload