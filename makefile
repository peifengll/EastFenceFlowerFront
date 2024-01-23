
run:
	python manage.py runserver 0.0.0.0:8000
newapp:
	python manage.py startapp  <app_name>

inreq:
	pip install -r requirements.txt -i -i https://mirrors.aliyun.com/pypi/simple

outreq:
	pip list --format=freeze> requirements.txt

# python manage.py inspectdb --database default tablename1 tablename2 >myApp/models.py
# python manage.py inspectdb  manager  >login/models.py

# python manage.py inspectdb    >models/models.py
