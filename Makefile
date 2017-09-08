#
# Makefile
# DEBUG OSX: verify /etc/exports using docker-machine-nfs
#


SHELL := /bin/bash
HIDE ?= @
IMAGE ?= drchrono/app
CONTAINER ?= drchrono
VOLUME ?= -v $(PWD):/drchrono/src

.PHONY: build image


build:
	$(HIDE)docker build -t $(IMAGE) .

start:
	$(HIDE)docker run --rm $(VOLUME) -it -p 8888:80 --name $(CONTAINER) $(IMAGE)

migrate:
	$(HIDE)docker run --rm $(VOLUME) -it $(IMAGE) python manage.py makemigrations
	$(HIDE)docker run --rm $(VOLUME) -it $(IMAGE) python manage.py migrate

test:
	$(HIDE)docker run --rm -it --name $(CONTAINER)-test $(IMAGE)

lint:
	$(HIDE)docker run --rm $(VOLUME) -it $(IMAGE) pep8 drchrono kiosk

enter:
	$(HIDE)docker exec -it $(CONTAINER) /bin/bash

clean:
	$(HIDE)find . -name "*.pyc" -exec rm -f {} \;
