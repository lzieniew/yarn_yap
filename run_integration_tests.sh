#!/usr/bin/env bash

function cleanup {
	echo "Stopping integration_tests_runner container..."
	docker stop integration_tests_runner
	docker rm integration_tests_runner
}

trap cleanup EXIT

docker-compose down
time env DUMMY_MODE=1 pytest integration_tests/test_integration.py
