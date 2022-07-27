resource "google_project" "default" {
  provider = google-beta

  project_id = "${local.project}-${var.environment}"
  name       = "${local.project}-${var.environment}"
}

resource "google_firebase_project" "default" {
  provider = google-beta
  project  = google_project.default.project_id
}