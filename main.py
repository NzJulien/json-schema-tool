import json
import sys
import argparse
from pathlib import Path
import anthropic


def load_json(path: str) -> dict:
    """Load and parse a JSON file."""
    with open(path, "r") as f:
        return json.load(f)


def generate_schema(data: dict) -> str:
    """Use Claude to generate a JSON schema from sample data."""
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"""Generate a valid JSON Schema (draft-07) for the following JSON data.
Return ONLY the JSON schema, no explanation or markdown.

Data:
{json.dumps(data, indent=2)}""",
            }
        ],
    )
    return message.content[0].text.strip()


def validate_against_schema(data: dict, schema: dict) -> str:
    """Use Claude to validate JSON data against a schema."""
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Validate the following JSON data against the given JSON Schema.
List any validation errors clearly. If valid, say "✅ Valid — data matches the schema."

Schema:
{json.dumps(schema, indent=2)}

Data:
{json.dumps(data, indent=2)}""",
            }
        ],
    )
    return message.content[0].text.strip()


def explain_schema(schema: dict) -> str:
    """Use Claude to explain a JSON schema in plain English."""
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Explain the following JSON Schema in plain English.
Describe what kind of data it expects, required fields, types, and any constraints.

Schema:
{json.dumps(schema, indent=2)}""",
            }
        ],
    )
    return message.content[0].text.strip()


def main():
    parser = argparse.ArgumentParser(
        description="AI-powered JSON Schema tool using Claude"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # generate command
    gen = subparsers.add_parser("generate", help="Generate a JSON schema from sample data")
    gen.add_argument("data", help="Path to sample JSON data file")
    gen.add_argument("-o", "--output", help="Save schema to this file")

    # validate command
    val = subparsers.add_parser("validate", help="Validate JSON data against a schema")
    val.add_argument("schema", help="Path to JSON schema file")
    val.add_argument("data", help="Path to JSON data file to validate")

    # explain command
    exp = subparsers.add_parser("explain", help="Explain a JSON schema in plain English")
    exp.add_argument("schema", help="Path to JSON schema file")

    args = parser.parse_args()

    if args.command == "generate":
        data = load_json(args.data)
        print(f"Generating schema for: {args.data}\n")
        schema_str = generate_schema(data)
        print(schema_str)
        if args.output:
            with open(args.output, "w") as f:
                f.write(schema_str)
            print(f"\n💾 Schema saved to {args.output}")

    elif args.command == "validate":
        schema = load_json(args.schema)
        data = load_json(args.data)
        print(f"Validating {args.data} against {args.schema}\n{'='*50}")
        result = validate_against_schema(data, schema)
        print(result)

    elif args.command == "explain":
        schema = load_json(args.schema)
        print(f"Explaining schema: {args.schema}\n{'='*50}")
        result = explain_schema(schema)
        print(result)


if __name__ == "__main__":
    main()
