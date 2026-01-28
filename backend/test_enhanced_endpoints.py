"""
Test script for Enhanced API Endpoints

This script tests the new admin API endpoints for enhanced anomaly detection.
"""

import requests
import json
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/admin"

# You'll need to replace this with a valid admin token
# Get it by logging in as an admin user
ADMIN_TOKEN = "YOUR_ADMIN_TOKEN_HERE"

headers = {
    "Authorization": f"Bearer {ADMIN_TOKEN}",
    "Content-Type": "application/json"
}


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_response(response: requests.Response, show_full: bool = False):
    """Print formatted response"""
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        if show_full:
            print(json.dumps(data, indent=2, default=str))
        else:
            # Print summary
            if isinstance(data, list):
                print(f"Results count: {len(data)}")
                if len(data) > 0:
                    print(f"First result: {json.dumps(data[0], indent=2, default=str)}")
            elif isinstance(data, dict):
                print(json.dumps(data, indent=2, default=str))
    else:
        print(f"Error: {response.text}")


def test_enhanced_metrics():
    """Test the enhanced metrics endpoint"""
    print_section("Testing Enhanced Metrics Endpoint")

    url = f"{BASE_URL}{API_PREFIX}/metrics/enhanced"
    print(f"GET {url}")

    response = requests.get(url, headers=headers)
    print_response(response, show_full=True)


def test_anomaly_breakdown():
    """Test the anomaly breakdown endpoint"""
    print_section("Testing Anomaly Breakdown Endpoint")

    # Test without time filter
    url = f"{BASE_URL}{API_PREFIX}/analytics/anomaly-breakdown"
    print(f"GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response, show_full=True)

    # Test with 24h filter
    print("\nWith 24h filter:")
    url_24h = f"{BASE_URL}{API_PREFIX}/analytics/anomaly-breakdown?time_period=24h"
    print(f"GET {url_24h}")
    response = requests.get(url_24h, headers=headers)
    print_response(response, show_full=True)


def test_anomalies_by_category():
    """Test the anomalies by category endpoint"""
    print_section("Testing Anomalies By Category Endpoint")

    categories = ["HALLUCINATION", "UNSAFE_ADVICE", "CONTEXT_MISMATCH", "POOR_QUALITY", "CONFIDENCE_ISSUE"]

    for category in categories:
        print(f"\nCategory: {category}")
        url = f"{BASE_URL}{API_PREFIX}/interactions/anomalies/by-category?category={category}&limit=5"
        print(f"GET {url}")

        response = requests.get(url, headers=headers)
        print_response(response)


def test_all_anomalies():
    """Test the all anomalies endpoint"""
    print_section("Testing All Anomalies Endpoint")

    # Without min_score
    url = f"{BASE_URL}{API_PREFIX}/interactions/anomalies/all?limit=10"
    print(f"GET {url}")
    response = requests.get(url, headers=headers)
    print_response(response)

    # With min_score
    print("\nWith min_score=0.7:")
    url_filtered = f"{BASE_URL}{API_PREFIX}/interactions/anomalies/all?limit=10&min_score=0.7"
    print(f"GET {url_filtered}")
    response = requests.get(url_filtered, headers=headers)
    print_response(response)


def test_detailed_analysis(interaction_id: str = None):
    """Test the detailed analysis endpoint"""
    print_section("Testing Detailed Analysis Endpoint")

    if not interaction_id:
        # First, get an interaction ID from all anomalies
        url = f"{BASE_URL}{API_PREFIX}/interactions/anomalies/all?limit=1"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                interaction_id = data[0]['id']
            else:
                print("No anomalies found to test with")
                return
        else:
            print("Failed to fetch anomaly for testing")
            return

    url = f"{BASE_URL}{API_PREFIX}/interactions/{interaction_id}/detailed"
    print(f"GET {url}")
    print(f"Interaction ID: {interaction_id}")

    response = requests.get(url, headers=headers)
    print_response(response, show_full=True)


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("  Enhanced API Endpoints Test Suite")
    print("=" * 80)

    if ADMIN_TOKEN == "YOUR_ADMIN_TOKEN_HERE":
        print("\n⚠️  WARNING: Please set a valid ADMIN_TOKEN in the script")
        print("You can get a token by:")
        print("1. Starting the server: uvicorn app.main:app --reload")
        print("2. Logging in as an admin user via the API")
        print("3. Copying the access token and pasting it in this script\n")
        return

    try:
        # Test 1: Enhanced Metrics
        test_enhanced_metrics()

        # Test 2: Anomaly Breakdown
        test_anomaly_breakdown()

        # Test 3: Anomalies by Category
        test_anomalies_by_category()

        # Test 4: All Anomalies
        test_all_anomalies()

        # Test 5: Detailed Analysis
        test_detailed_analysis()

        print_section("All Tests Completed")

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API")
        print("Make sure the server is running on http://localhost:8000")
        print("Start it with: uvicorn app.main:app --reload")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
