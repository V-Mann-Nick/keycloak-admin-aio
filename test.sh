#!/usr/bin/env bash

version=latest
while getopts ":v:" opt; do
  case $opt in
    v) version="$OPTARG"
    ;;
  esac
done

if command -v podman >/dev/null 2>&1; then
  container=podman
fi 

if command -v docker >/dev/null 2>&1; then
  container=docker
fi

if [ -z "$container" ]; then
  echo -e '❓ No container runtime found. Requires either docker or podman.'
  exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
  echo -e '❓ curl is required to test Keycloak'
  exit 1
fi

# Start keycloak detached
echo -e "🚀 Starting Keycloak ${version}"
container_id=$($container run \
-d \
--rm \
--env KEYCLOAK_ADMIN=testing \
--env KEYCLOAK_ADMIN_PASSWORD=testing \
--env KC_HEALTH_ENABLED=true \
-p 8080:8080 \
quay.io/keycloak/keycloak:${version} \
start-dev
)

# Cleanup container on exit
function cleanup() {
  echo -e '🧹 Stopping Keycloak'
  $container rm -f $container_id >/dev/null
}
trap cleanup EXIT

# Poll Keycloak for 1m until it's ready otherwise exit with error
is_ready=false
for i in {1..60}; do
  if curl -s http://localhost:8080/health >/dev/null; then
    is_ready=true
    echo -e '✅ Keycloak is ready'
    break
  fi
  echo -e '🕑 Waiting for Keycloak to start'
  sleep 1
done
if [ "$is_ready" = false ]; then
  echo -e '❌ Keycloak failed to start'
  exit 1
fi

# Run tests
echo -e '🧪 Running tests'
poetry run poe pytest
