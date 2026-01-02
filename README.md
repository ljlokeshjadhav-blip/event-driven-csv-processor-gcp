# event-driven-csv-processor-gcp
Event-driven CSV processing using GCS, Pub/Sub, and Cloud Run
=====================================================================================================================================================
# Cloud Storage Triggered CSV Processor

## Overview
This project implements an event-driven data pipeline on Google Cloud.

When a CSV file is uploaded to a GCS bucket:
1. Cloud Storage sends an event to Pub/Sub
2. Pub/Sub triggers a Cloud Run service
3. The service processes the CSV using Pandas
4. Metrics are written as a JSON file back to GCS
5. Firestore is used for idempotency

## Features
- Event-driven architecture
- Processes only CSV files
- Row count and null count metrics
- Retry & idempotency using Firestore
- Serverless & scalable
- CI/CD using Cloud Build

## Tech Stack
- Google Cloud Storage
- Pub/Sub
- Cloud Run
- Firestore
- Cloud Build
- Python, Pandas

## Deployment
Deployment is automated via Cloud Build on merge to `develop` branch.

