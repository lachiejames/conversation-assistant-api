resource "google_storage_bucket" "bucket" {
  name     = "${var.project}-${var.environment}-bucket-${var.function_name}"
  location = "US"
}

resource "google_storage_bucket_object" "archive" {
  name   = "${var.function_name}.zip"
  bucket = google_storage_bucket.bucket.name
  source = "../main.py"
}

resource "google_cloudfunctions_function" "function" {
  name        = "${var.function_name}-function"
  description = "Generates message suggestions for a user to respond with based upon their conversation history, and some context parameters"
  runtime     = "python39"

  available_memory_mb          = 128
  source_archive_bucket        = google_storage_bucket.bucket.name
  source_archive_object        = google_storage_bucket_object.archive.name
  trigger_http                 = true
  https_trigger_security_level = "SECURE_ALWAYS"
  timeout                      = 60
  entry_point                  = "generate_suggestions"
  # labels = {
  #   my-label = "my-label-value"
  # }

  # environment_variables = {
  #   MY_ENV_VAR = "my-env-var-value"
  # }
}

# # IAM entry for a single user to invoke the function
# resource "google_cloudfunctions_function_iam_member" "invoker" {
#   project        = google_cloudfunctions_function.function.project
#   region         = google_cloudfunctions_function.function.region
#   cloud_function = google_cloudfunctions_function.function.name

#   role   = "roles/cloudfunctions.invoker"
#   member = "user:myFunctionInvoker@example.com"
# }
