FLASK_APP=app.py

run:
	export FLASK_APP=$(FLASK_APP)
	flask run

install:
	pip3 install -r requirements.txt

.PHONY: run install