#!/bin/bash

# Function to update image version in YAML file
update_image_version() {
  local file=$1
  local service=$2
  local current_version=$(grep "image: mreider/$service:" $file | awk -F: '{print $3}')
  if [ -z "$current_version" ]; then
    echo "Current version not found for $service in $file"
    exit 1
  fi
  local new_version=$((current_version + 1))
  sed -i "s/image: mreider\/$service:$current_version/image: mreider\/$service:$new_version/" $file
  echo $new_version
}

# Update image versions in YAML files
new_wash_version=$(update_image_version "k8s/wash.yaml" "wash")
new_dry_version=$(update_image_version "k8s/dry.yaml" "dry")
new_disk_cleaner_version=$(update_image_version "k8s/disk-cleaner.yaml" "disk-cleaner")
new_waterfall_version=$(update_image_version "k8s/waterfall.yaml" "waterfall")

# Build and push Docker images

sudo docker buildx build --no-cache --platform linux/amd64,linux/arm64 -t mreider/wash:$new_wash_version -f wash/Dockerfile --push .

sudo docker buildx build --no-cache --platform linux/amd64,linux/arm64 -t mreider/dry:$new_dry_version -f dry/Dockerfile--push .

sudo docker buildx build --no-cache --platform linux/amd64,linux/arm64 -t mreider/disk_cleaner:$new_disk_cleaner_version -f disk_cleaner/Dockerfile --push .

sudo docker buildx build --no-cache --platform linux/amd64,linux/arm64 -t mreider/waterfall:$new_waterfall_version -f waterfall/Dockerfile --push .

# Commit changes to GitHub
git add .
git commit -m "version $new_wash_version"
git push origin main
