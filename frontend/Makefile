docker-build:
	if [ -d './build' ]; then rm build -r; fi
	npm run build
	sudo docker build . -t ${IMG}

docker-push:
	sudo docker push ${IMG}