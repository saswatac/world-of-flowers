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
	  --set-env-vars=GEO_DB_PATH=$${GEO_DB_PATH},IMAGE_STORAGE_PATH=$${IMAGE_STORAGE_PATH},ADMIN_USERS=$${ADMIN_USERS}
