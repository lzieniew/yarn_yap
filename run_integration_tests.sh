#!/usr/bin/env bash

function cleanup {
	echo "Stopping integration_tests_runner container..."
	docker stop integration_tests_runner
	docker rm integration_tests_runner
}

trap cleanup EXIT

docker-compose up -d --build -e DUMMY_MODE=1

docker build -t integration_tests_runner -f ./integration_tests/Dockerfile_integration_tests .
docker run --privileged --name integration_tests_runner -v /var/run/docker.sock:/var/run/docker.sock -v "$(pwd):/app" -d integration_tests_runner

docker logs -f integration_tests_runner
