resource "google_storage_bucket" "terraform_test" {
    name     = "ecommerce-terraform-test-bucket-511117"
    location = "us-central1"
    force_destroy = true

    lifecycle_rule {
        condition{
            age=1
        }
        action{
            type="Delete"
        }
    }
}