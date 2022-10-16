resource "google_storage_bucket" "bucket_android_assets" {
  name     = "${local.project}-${var.environment}-bucket-android-assets"
  location = "US"
}

resource "google_storage_bucket_object" "simple_gmail" {
  name = "simple_gmail.gif"
  source       = "../assets/simple_gmail.gif"
  bucket       = google_storage_bucket.bucket_android_assets.name
}
