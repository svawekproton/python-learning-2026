# CSV User Processor

Filter and sort users from CSV by email domain.

## Usage

```bash
# Default (gmail.com)
python csv_processor.py

# Custom domain
python csv_processor.py --domain yahoo.com

# Help
python csv_processor.py --help
```

## Input (users.csv)

```csv
id,name,email
1,Alice Johnson,alice.johnson@gmail.com
2,Bob Smith,bob.smith@yahoo.com
```

## Output
Console + output.json:
```json
[
  {
    "id": "1",
    "name": "Alice Johnson",
    "email": "alice.johnson@gmail.com"
  }
]
```

## Features

- ✅ CLI arguments (argparse)
- ✅ Error handling
- ✅ Input validation
- ✅ Alphabetical sorting
- ✅ JSON output (pretty-printed)

## Requirements

Python 3.7+ (no external dependencies)

## What I Learned

- Python syntax vs Ruby
- CSV + JSON modules
- argparse for CLI
- List comprehensions
- Error handling (try/except)
- `if __name__ == "__main__"`