terraform{
    required_providers{
        google = {
            source = "hashicorp/google"
            version = "~> 5.0"
        }
    }
}
provider "google" {
    project = "ecommerce-data-pipeline-511117"
    region = "us-central"
}