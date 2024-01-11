.PHONY: deps-init
deps-init:
	echo "INFO: creating dependencies..."
	@docker-compose up -d --build
	@bash ./scripts/init-dep.sh ./scripts/init-vault ./schema/vault ./scripts/init-es ./schema/elasticsearch
	
.PHONY: deps-tear
deps-tear:
	@docker-compose down --volumes --remove-orphans

.PHONY: migrate-up
migrate-up:
	@bash ./scripts/migrate.sh upgrade

.PHONY: migrate-down
migrate-down:
	@bash ./scripts/migrate.sh downgrade

.PHONY: run-local
run-local:
	python app.py

.PHONY: test
test:
	python -m unittest discover -p '*_test.py'