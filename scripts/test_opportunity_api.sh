#!/bin/bash

API_URL="http://localhost:8000/api/v1/opportunities"

print_separator() {
    echo "=============================="
    echo "$1"
    echo "=============================="
}

make_api_call() {
    local method=$1
    local url=$2
    local data=$3
    local expected_status=$4

    echo "Making $method request to $url"
    if [ ! -z "$data" ]; then
        echo "Request data: $data"
    fi

    if [ ! -z "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" \
            -H "Content-Type: application/json" \
            -d "$data")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url")
    fi

    body=$(echo "$response" | sed '$d')
    status_code=$(echo "$response" | tail -n1)

    echo "Response status code: $status_code"
    echo "Response body: $body"

    if [ "$status_code" -eq "$expected_status" ]; then
        echo "Request successful"
        return 0
    else
        echo "Request failed with status $status_code"
        return 1
    fi
}

# Create Opportunity
print_separator "Creating Opportunity"
opp_data='{
    "name": "Shell Opportunity",
    "description": "Created via shell script",
    "stage": "Prospecting",
    "amount": 5000.0,
    "close_date": "2025-12-31T00:00:00Z",
    "is_won": false
}'

if make_api_call "POST" "$API_URL" "$opp_data" 201; then
    opp_id=$(echo "$body" | jq -r '._id')
    if [ -z "$opp_id" ] || [ "$opp_id" = "null" ]; then
        echo "Failed to extract opportunity ID from response"
        exit 1
    fi
    echo "Created opportunity with ID: $opp_id"
else
    echo "Failed to create opportunity"
    exit 1
fi

# List Opportunities
print_separator "Listing Opportunities"
make_api_call "GET" "$API_URL" "" 200

# Get Opportunity
print_separator "Getting Opportunity by ID"
make_api_call "GET" "$API_URL/$opp_id" "" 200

# Update Opportunity
print_separator "Updating Opportunity"
update_data='{"name": "Updated Shell Opp", "description": "Updated via shell"}'
make_api_call "PATCH" "$API_URL/$opp_id" "$update_data" 200

# Filter by Name
print_separator "Filtering Opportunities by Name"
make_api_call "GET" "$API_URL?name=Updated%20Shell%20Opp" "" 200

# Delete Opportunity
print_separator "Deleting Opportunity"
make_api_call "DELETE" "$API_URL/$opp_id" "" 204

# Confirm Deletion
print_separator "Confirming Deletion"
make_api_call "GET" "$API_URL/$opp_id" "" 404 