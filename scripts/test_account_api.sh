#!/bin/bash

# Set the API URL
API_URL="http://localhost:8000/api/v1/accounts"

# Function to print a separator
print_separator() {
    echo "=============================="
    echo "$1"
    echo "=============================="
}

# Function to make API calls with better error handling
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
    
    # Split response into body and status code
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

# Create Account
print_separator "Creating Account"
account_data='{
    "name": "Test Company",
    "description": "A test company",
    "website_url": "https://testcompany.com",
    "industry": "Technology",
    "employee_count": 100,
    "annual_revenue": 1000000,
    "is_active": true
}'

if make_api_call "POST" "$API_URL" "$account_data" 201; then
    # Extract account ID from response
    account_id=$(echo "$body" | jq -r '._id')
    if [ -z "$account_id" ] || [ "$account_id" = "null" ]; then
        echo "Failed to extract account ID from response"
        exit 1
    fi
    echo "Created account with ID: $account_id"
else
    echo "Failed to create account"
    exit 1
fi

# List Accounts
print_separator "Listing Accounts"
if ! make_api_call "GET" "$API_URL" "" 200; then
    echo "Failed to list accounts"
    exit 1
fi

# Get Account
print_separator "Getting Account"
if ! make_api_call "GET" "$API_URL/$account_id" "" 200; then
    echo "Failed to get account"
    exit 1
fi

# Update Account
print_separator "Updating Account"
update_data='{
    "name": "Updated Test Company",
    "description": "An updated test company"
}'
if ! make_api_call "PATCH" "$API_URL/$account_id" "$update_data" 200; then
    echo "Failed to update account"
    exit 1
fi

# Delete Account
print_separator "Deleting Account"
if ! make_api_call "DELETE" "$API_URL/$account_id" "" 204; then
    echo "Failed to delete account"
    exit 1
fi

echo "All tests completed successfully!" 