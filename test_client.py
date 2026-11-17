import requests

URL = "http://localhost:5001/validate"


# Send one request, print the response, and return True if it matches.
def show_result(title, payload, expected=None):
    print(title)
    response = requests.post(URL, json=payload)
    result = response.json()
    print(result)

    if expected is None:
        print()
        return True

    if result == expected:
        print("PASS")
        print()
        return True

    print("FAIL")
    print("expected:", expected)
    print()
    return False


checks = []

# 1. Required field has a value.
checks.append(show_result(
    "Valid data: color_code is filled in",
    {
        "data": {
            "color_code": "H2"
        },
        "rules": {
            "color_code": {"required": True}
        }
    },
    {"valid": True, "errors": []}
))

# 2. Required field is missing.
checks.append(show_result(
    "Missing required field: color_code",
    {
        "data": {
            "quantity": 10
        },
        "rules": {
            "color_code": {"required": True}
        }
    },
    {"valid": False, "errors": ["color_code is required"]}
))

# 3. Required field is empty.
checks.append(show_result(
    "Empty required field: color_code",
    {
        "data": {
            "color_code": ""
        },
        "rules": {
            "color_code": {"required": True}
        }
    },
    {"valid": False, "errors": ["color_code cannot be empty"]}
))

# 4. Number is high enough.
checks.append(show_result(
    "Valid number: quantity meets the minimum",
    {
        "data": {
            "quantity": 10
        },
        "rules": {
            "quantity": {"min": 0}
        }
    },
    {"valid": True, "errors": []}
))

# 5. Number is too small.
checks.append(show_result(
    "Negative number: quantity is below the minimum",
    {
        "data": {
            "quantity": -10
        },
        "rules": {
            "quantity": {"min": 0}
        }
    },
    {"valid": False, "errors": ["quantity must be at least 0"]}
))

# 6. Value is not a number.
checks.append(show_result(
    "Non-numeric value: quantity is text",
    {
        "data": {
            "quantity": "abc"
        },
        "rules": {
            "quantity": {"min": 0}
        }
    },
    {"valid": False, "errors": ["quantity must be a number"]}
))

# 7. Multiple validation errors.
checks.append(show_result(
    "Multiple validation errors",
    {
        "data": {
            "color_code": "",
            "quantity": -10
        },
        "rules": {
            "color_code": {"required": True},
            "quantity": {"required": True, "min": 0}
        }
    },
    {
        "valid": False,
        "errors": [
            "color_code cannot be empty",
            "quantity must be at least 0"
        ]
    }
))

if False in checks:
    raise SystemExit(1)

