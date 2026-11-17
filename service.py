from flask import Flask, jsonify, request

app = Flask(__name__)
# Keep "valid" before "errors" in the JSON.
app.json.sort_keys = False


# The number 0 is not empty.
def is_empty(value):
    if value is None:
        return True

    if isinstance(value, str) and value.strip() == "":
        return True

    return False


# True and False are not numbers.
def is_number(value):
    if isinstance(value, bool):
        return False

    return isinstance(value, (int, float))


def validate_required_fields(data, rules):
    errors = []

    for field_name in rules:
        field_rules = rules[field_name]

        if not isinstance(field_rules, dict):
            continue

        if field_rules.get("required") is True:
            if field_name not in data:
                errors.append(field_name + " is required")
            elif is_empty(data[field_name]):
                errors.append(field_name + " cannot be empty")

    return errors


def validate_min_values(data, rules):
    errors = []

    for field_name in rules:
        field_rules = rules[field_name]

        if not isinstance(field_rules, dict):
            continue

        if "min" not in field_rules:
            continue

        if field_name not in data or is_empty(data[field_name]):
            continue

        value = data[field_name]
        minimum = field_rules["min"]

        if not is_number(value):
            errors.append(field_name + " must be a number")
            continue

        if not is_number(minimum):
            errors.append(field_name + " has an invalid minimum")
            continue

        if value < minimum:
            errors.append(field_name + " must be at least " + str(minimum))

    return errors


@app.route("/validate", methods=["POST"])
def validate():
    body = request.get_json(silent=True)

    if not isinstance(body, dict):
        return jsonify({
            "valid": False,
            "errors": ["Request body must be a JSON object with data and rules."]
        })

    data = body.get("data")
    rules = body.get("rules")

    if not isinstance(data, dict) or not isinstance(rules, dict):
        return jsonify({
            "valid": False,
            "errors": ["Request must include data and rules objects."]
        })

    errors = validate_required_fields(data, rules)
    errors.extend(validate_min_values(data, rules))

    if len(errors) == 0:
        return jsonify({
            "valid": True,
            "errors": []
        })

    return jsonify({
        "valid": False,
        "errors": errors
    })


if __name__ == "__main__":
    app.run(port=5001, debug=True)
