BIN_DIR=$(shell pwd)
env:
	pip3 install --upgrade python==3.11.3 -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
init:
	pip3 install -r $(BIN_DIR)/server/requirements.txt
	cd $(BIN_DIR)/client; npm install
	cd $(BIN_DIR)/server_mp; pip3 install -r requirements.txt
all:
	python3 $(BIN_DIR)/server/manage.py runserver 8000 &
	cd $(BIN_DIR)/server; celery -A server worker -l info --beat &
	cd $(BIN_DIR)/server_mp; scrapyd-deploy -p server_mp &
	cd $(BIN_DIR)/server_mp; scrapyd
run_client:
	cd $(BIN_DIR)/client; npm run dev
run_dev:
	python3 $(BIN_DIR)/server/manage.py runserver 8000 &
	cd $(BIN_DIR)/server; celery -A server worker -l info --beat &
	cd $(BIN_DIR)/server_mp; scrapyd-deploy -p server_mp &
	cd $(BIN_DIR)/client; npm run dev &
	cd $(BIN_DIR)/server_mp; scrapyd
