DOCKERIMAGENAME ?= snowapi
APIPORT ?= 8080

docker:
	DOCKER_BUILDKIT=1 docker build -f ./Dockerfile --no-cache --progress=plain  -t $(DOCKERIMAGENAME) .

run:
	docker run -p $(APIPORT):$(APIPORT) $(DOCKERIMAGENAME)

run_local:
	cd snow_rest && python app.py
