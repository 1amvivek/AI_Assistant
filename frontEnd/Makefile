help:
	@echo targets are: clean pull-image run-mongo run-app-interactive run-app-detached run-all help

pull-image:
	docker pull cnkdock1890/arya

run-mongo:
	docker run --name mongo -td -p 27017:27017 mongo

run-app-interactive:
	docker run -it -p 3000:3000 --name arya_interactive --link mongo cnkdock1890/arya

run-app-detached:
	docker run -td -p 3000:3000 --name arya_detached --link mongo cnkdock1890/arya

run-all: pull-image run-app-detached

run-all-hard: pull-image run-mongo run-app-detached

clean:
	-docker rm -f arya_detached arya_interactive
	-docker rmi mongo:latest
	-docker rmi cnkdock1890/arya

clean-hard:
	-docker rm -f arya_detached arya_interactive mongo
	-docker rmi mongo:latest
	-docker rmi cnkdock1890/arya

.PHONY: clean pull-image run-mongo run-app-interactive run-app-detached run-all
