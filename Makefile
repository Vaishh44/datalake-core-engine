# Makefile for Data Lake Engine (Phase 1: Ozone)

.PHONY: up-ozone down-ozone test-ozone logs-ozone clean

# Start Ozone Only (Phase 1)
up-ozone:
	@echo "Starting Apache Ozone (Phase 1)..."
	docker-compose -f docker-compose.ozone.yml up -d
	@echo "Waiting for services to initialize..."

# Stop Ozone
down-ozone:
	@echo "Stopping Ozone..."
	docker-compose -f docker-compose.ozone.yml down

# View Logs
logs-ozone:
	docker-compose -f docker-compose.ozone.yml logs -f ozone-om

# Run Verification Script
test-ozone:
	@echo "Running Ozone Verification Script..."
	python3 verify_ozone.py

# Install python dependencies
install-deps:
	pip3 install boto3 requests

# Full System (For later phases)
up-all:
	docker-compose up -d

down-all:
	docker-compose down
