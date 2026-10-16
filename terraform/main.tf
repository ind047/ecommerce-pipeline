resource "google_storage_bucket" "raw_data"{
    name     = "ecommerce-data-pipeline-511117-raw-data"
    location = "us-central1"
    force_destroy = false
}