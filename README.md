# 🗂️ JSON Schema AI Tool

An AI-powered CLI tool that uses Claude to **generate**, **validate**, and **explain** JSON Schemas.

## Features

- **Generate** a JSON Schema from any sample JSON data
- **Validate** JSON data against an existing schema
- **Explain** any JSON Schema in plain English

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/NzJulien/json-schema-tool.git
   cd json-schema-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Anthropic API key**
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

### Generate a schema from sample data
```bash
python main.py generate sample_data.json
python main.py generate sample_data.json -o schema.json   # save to file
```

### Validate data against a schema
```bash
python main.py validate schema.json data.json
```

### Explain a schema in plain English
```bash
python main.py explain schema.json
```

## Example

```bash
$ python main.py generate sample_data.json
Generating schema for: sample_data.json

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "name", "email"],
  ...
}
```

## Requirements

- Python 3.8+
- Anthropic API key (get one at https://console.anthropic.com)

## License

MIT
