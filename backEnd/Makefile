help:
	@echo targets are: build run build-clean

build:
	virtualenv -p python venv

install:
	( \
		source venv/bin/activate; \
		pip install -r requirements; \
	)

run:
	python app.py >> flask_logger.log 2>&1

build-clean:
	rm -rf ./venv

.PHONY: build run build-clean activate-venv
