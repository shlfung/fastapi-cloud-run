How to deploy fastapi on google cloud run

https://codelabs.developers.google.com/codelabs/cloud-run-hello-python3/index.html?index=..%2F..index#0

1.) Create a Project on Google Cloud

2.) Set glcoud to the project
gcloud config set project <PROJECT_ID>


3.) Enable the APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com

4.) Set the PROJECT_ID and DOCKER_IMG

PROJECT_ID=$(gcloud config get-value project)
echo $PROJECT_ID

DOCKER_IMG="gcr.io/$PROJECT_ID/fastapi-cloud-run"
echo $DOCKER_IMG

5.) Build container image using Cloud Build
gcloud builds submit --tag $DOCKER_IMG

