export-globals:
	sh ./kinoreel_backend/settings/export_globals.sh

build-image:
	docker build -t kino-backend \
	--build-arg PG_SERVER="${PG_SERVER}" \
	--build-arg PG_PORT="${PG_PORT}" \
	--build-arg PG_DB="${PG_DB}" \
	--build-arg PG_USERNAME="${PG_USERNAME}" \
	--build-arg PG_PASSWORD="${PG_PASSWORD}" \
	--build-arg ALLOWED_HOST="${ALLOWED_HOST}" \
	.

run-image:
	docker run -p 3001:8000 -d kino-backend

push-image:
	docker tag kino-backend unrufflednightingale/kino-backend:latest
	docker push unrufflednightingale/kino-backend:latest

build-and-push-image: export-globals build-image push-image