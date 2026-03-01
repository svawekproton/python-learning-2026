# Custom Logger with Decorators

A Python-native logging system demonstrating OOP, Enum usage, decorators, and testing with pytest.

## Usage

```python
from logger import Logger
from decorators import login_required, log_execution_time

# Initialize logger (configurable outputs)
log = Logger(print_console=True, save_to_log=True, user_logined=True)

# Log messages with different severity levels
log.info("System initialized")
log.warning("High memory usage")
log.error("Database connection failed")
```

## Output
Console + logs.log:
```text
2026-03-01T15:00:00.000000+00:00 - INFO - System initialized
Finished _format_message() in 0.0001 secs
2026-03-01T15:00:00.005000+00:00 - ERROR - Database connection failed
Finished _format_message() in 0.0001 secs
```

## Features

- ✅ OOP Design: Encapsulated logging logic with configurable file/console outputs.
- ✅ Type Safety: Using Enum and type hints (-> None, : str) to prevent magic strings.
- ✅ Decorators:
      @log_execution_time to measure runtime (time.perf_counter()).
      @login_required to demonstrate fail-fast authorization (PermissionError).
- ✅ Testing: Fully tested with pytest (using tmp_path, capsys, and exception assertions).

## Requirements

Python 3.11+
pytest (for running tests)

## What I Learned (Ruby vs Python differences)

- self is explicitly required as the first argument in class methods.
- No const keyword — constants are uppercase by convention or handled via Enum.
- Python Decorators vs Ruby Wrappers (functools.wraps is essential).
- pytest fixtures (tmp_path, capsys) instead of RSpec's let and describe.
