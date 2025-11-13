terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
  credentials = file(var.credentials_file)
}

resource "google_compute_network" "vpc_network" {
  name = "app-network"
}

resource "google_compute_firewall" "default" {
  name    = "allow-http-ssh"
  network = google_compute_network.vpc_network.self_link

  allow {
    protocol = "tcp"
    ports    = ["22", "80", "8080"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_instance" "python_vm" {
  name         = "python-vm"
  machine_type = "e2-medium"
  zone         = var.zone
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }
  network_interface {
    network = google_compute_network.vpc_network.self_link
    access_config {}
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    apt-get update
    apt-get install -y docker.io
    systemctl enable docker
    systemctl start docker
  EOT
}

resource "google_compute_instance" "java_vm" {
  name         = "java-vm"
  machine_type = "e2-medium"
  zone         = var.zone
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }
  network_interface {
    network = google_compute_network.vpc_network.self_link
    access_config {}
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    apt-get update
    apt-get install -y docker.io
    systemctl enable docker
    systemctl start docker
  EOT
}

output "python_vm_ip" {
  value = google_compute_instance.python_vm.network_interface[0].access_config[0].nat_ip
}

output "java_vm_ip" {
  value = google_compute_instance.java_vm.network_interface[0].access_config[0].nat_ip
}
