docker-repo := "192.168.1.101:5000"
image-name := "quotebot"
image-tag := "latest"

build:
	docker build --platform linux/arm64 -t {{docker-repo}}/{{image-name}}:{{image-tag}} .

push:
	docker push {{docker-repo}}/{{image-name}}:{{image-tag}}

start-db:
	docker compose -f docker-compose.local.yml up -d

stop-db:
	docker compose -f docker-compose.local.yml down

start-dev:
	poetry run python src/bot.py
