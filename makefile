
run:
	python manage.py runserver 0.0.0.0:8000
newapp:
	python manage.py startapp  $(name)

inreq:
	pip install -r requirements.txt  -i https://mirrors.aliyun.com/pypi/simple

outreq:
	pip list --format=freeze> requirements.txt

# 强制拉取最新分支覆盖到本地
force:
	git fetch --all
	git reset --hard origin/main
	git pull

# python manage.py inspectdb --database default tablename1 tablename2 >myApp/models.py
# python manage.py inspectdb  manager  >login/models.py

# python manage.py inspectdb    >models/a.py
