# Logging Guidelines

> How logging is done in this Django project.

---

## Overview

This project uses Python's standard `logging` module configured through Django's `LOGGING` setting. Logs are output to console for both development and production.

---

## Log Configuration

### Base Configuration

```python
# config/settings/base.py
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
        "rich": {"datefmt": "[%X]"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "loggers": {
        "django": {
            "handlers": [],
            "level": "INFO",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}
```

---

## Log Levels

| Level | When to Use |
|-------|-------------|
| `DEBUG` | Detailed information for debugging (only in development) |
| `INFO` | Confirmation that things are working as expected |
| `WARNING` | Something unexpected happened, but the software is still working |
| `ERROR` | Due to a more serious problem, the software has not been able to perform some function |
| `CRITICAL` | A serious error, indicating that the program itself may be unable to continue running |

### Usage Examples

```python
import logging

logger = logging.getLogger(__name__)

# Debug - detailed diagnostic information
logger.debug(f"Processing post {post_id} with status {status}")

# Info - normal operational events
logger.info(f"User {user.username} logged in successfully")

# Warning - unexpected but recoverable
logger.warning(f"Slow query detected: {query} took {duration}s")

# Error - serious problem, functionality affected
logger.error(f"Failed to send email to {email}: {str(e)}")

# Critical - system-level failure
logger.critical("Database connection lost, application may be unavailable")
```

---

## What to Log

### Always Log

1. **Authentication events**: Login, logout, failed login attempts
2. **Authorization failures**: Permission denied events
3. **Business-critical operations**: Post creation, comment submission
4. **External service calls**: Email sending, third-party API calls
5. **Background tasks**: Huey task start, completion, failure
6. **Performance issues**: Slow queries, timeout warnings

### Example for Huey Tasks

```python
# dream_blog/core/tasks.py
import logging
from huey.contrib.djhuey import task

logger = logging.getLogger(__name__)

@task()
def send_notification_email(user_id, subject, body):
    logger.info(f"Starting email task for user {user_id}")
    try:
        # Send email logic
        logger.info(f"Email sent successfully to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send email to user {user_id}: {str(e)}")
        raise
```

---

## What NOT to Log

### Never Log

1. **Passwords**: Even hashed passwords should not be logged
2. **API keys and secrets**: Never log authentication tokens
3. **Personal Identifiable Information (PII)**: SSN, credit card numbers, etc.
4. **Complete request bodies**: May contain sensitive data
5. **Session tokens**: Could be used for session hijacking

### Safe Logging Patterns

```python
# BAD - logs sensitive data
logger.info(f"User logged in with password: {password}")

# GOOD - logs only necessary info
logger.info(f"User {user.username} logged in successfully")

# BAD - logs full request body
logger.debug(f"Request body: {request.body}")

# GOOD - logs only relevant fields
logger.debug(f"Request content_type: {request.POST.get('content_type')}")
```

---

## Structured Logging

### Format

The verbose formatter outputs:
```
%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s
```

Example output:
```
INFO 2024-01-15 10:30:45,123 views 12345 67890 User john logged in successfully
```

### Adding Context

Include relevant IDs and context in log messages:

```python
# BAD - vague message
logger.error("Failed to process request")

# GOOD - includes context
logger.error(f"Failed to process comment {comment_id} for post {post_id}: {str(e)}")
```

---

## Common Mistakes

### Using print() instead of logging

```python
# BAD
print(f"Debug info: {value}")

# GOOD
logger.debug(f"Debug info: {value}")
```

### Not using __name__ for logger

```python
# BAD - uses root logger directly
logging.info("Message")

# GOOD - uses module-specific logger
logger = logging.getLogger(__name__)
logger.info("Message")
```

### Logging at wrong level

```python
# BAD - using ERROR for expected conditions
logger.error("User not found")  # This is expected, use INFO or WARNING

# GOOD - appropriate level
logger.info(f"User lookup: no user found with email {email}")
```
