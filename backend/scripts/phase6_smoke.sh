#!/usr/bin/env bash
set -euo pipefail

API_BASE=${API_BASE:-http://localhost:8000}
ADMIN_EMAIL=${ADMIN_EMAIL:-admin1234@example.com}
ADMIN_PASSWORD=${ADMIN_PASSWORD:-admin123}

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required for this script. Install via: brew install jq" >&2
  exit 1
fi

login() {
  curl -sS "$API_BASE/api/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$1\",\"password\":\"$2\"}" | jq -r .access_token
}

token=$(login "$ADMIN_EMAIL" "$ADMIN_PASSWORD")
if [[ -z "$token" || "$token" == "null" ]]; then
  echo "Failed to login as admin." >&2
  exit 1
fi

echo "Admin token acquired."

echo "\nAll interactions:"
curl -sS "$API_BASE/api/admin/interactions" \
  -H "Authorization: Bearer $token" | jq '.[0]'

echo "\nFlagged interactions:"
curl -sS "$API_BASE/api/admin/interactions/flagged" \
  -H "Authorization: Bearer $token" | jq '.[0]'

echo "\nAdmin users:"
curl -sS "$API_BASE/api/admin/users" \
  -H "Authorization: Bearer $token" | jq '.[] | select(.role == "admin")' | head -n 1
