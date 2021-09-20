serve_backend:
	cd functions && PORT=8081 functions_framework --target=app --host 0.0.0.0

serve_frontend:
	yarn serve

deploy:
	gcloud functions deploy world_of_flowers \
	  --entry-point app \
	  --runtime python38 \
	  --trigger-http \
	  --allow-unauthenticated \
	  --project saswatalabs \
	  --region asia-south1 \
	  --source functions \
	  --set-env-vars=GEO_DB_PATH=gs://sc-world-of-flowers-db-test/db.geojson,IMAGE_STORAGE_PATH=gs://sc-world-of-flowers-test/images,ADMIN_USERS=saswata.123@gmail.com



