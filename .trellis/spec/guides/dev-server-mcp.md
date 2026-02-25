# dev-manager-mcp Integration Guide

> Guide for AI agents on using dev-manager-mcp for development server management.

---

## Overview

**dev-manager-mcp** is an MCP daemon that manages development servers with automatic port allocation, avoiding port conflicts across multiple projects.

**Key Features:**
- Auto-allocates ports starting at 3010
- Manages server lifecycle (start/stop/status/tail)
- Passes port via `PORT` environment variable
- Auto-cleanup after 120s idle timeout

**Installation:**

Start daemon (user's responsibility):
```bash
npx -y dev-manager-mcp
```

MCP client config (user's global config):
```json
{
  "mcpServers": {
    "dev-manager": {
      "command": "npx",
      "args": ["dev-manager-mcp", "stdio"]
    }
  }
}
```

---

## When to Use

Use dev-manager-mcp when you need to:
- Start a dev server for testing changes
- Run a server alongside other projects
- Verify frontend-backend integration
- Test with Playwright or browser automation

**Do NOT use for:**
- One-off commands that don't start a server
- Database migrations or management commands
- Static file operations

---

## MCP Tools

### `start` - Start a Development Server

```python
mcp__dev-manager__start(command="python manage.py runserver", cwd="/path/to/project")
# Returns: { "status": "started", "port": 3010, "session_key": "A3X9" }
```

**Parameters:**
- `command` (required): Shell command to execute
- `cwd` (optional): Working directory (defaults to client's working directory)

**Returns:**
- `status`: "started"
- `port`: Allocated port number
- `session_key`: Unique session identifier (4 chars)

### `stop` - Stop a Running Server

```python
mcp__dev-manager__stop(session_key="A3X9")
# Returns: { "status": "stopped", "session_key": "A3X9" }
```

### `status` - Check Server Status

```python
mcp__dev-manager__status(session_key="A3X9")  # Specific session
mcp__dev-manager__status()                    # All sessions
```

### `tail` - Get Server Logs

```python
mcp__dev-manager__tail(session_key="A3X9")
# Returns: { "session_key": "A3X9", "stdout": "...", "stderr": "" }
```

---

## Project-Specific Commands

### Vite Frontend (Start First)

```python
# Start Vite server first to get allocated port
# Try pnpm first, fallback to npm if pnpm fails
mcp__dev-manager__start(
    command="pnpm dev",
    cwd="/home/yxg/Workspace/django-dream-blog/frontend"
)
# If pnpm fails with "not found", retry with:
mcp__dev-manager__start(
    command="npm run dev",
    cwd="/home/yxg/Workspace/django-dream-blog/frontend"
)
# Returns: { "status": "started", "port": 3011, "session_key": "A3X9" }
```

**Note**: MCP daemon runs in its own environment. If pnpm fails with "not found" error, use `npm run dev` instead. Both package managers are configured in package.json.

Vite is configured to read `process.env.PORT` in `vite.config.js`, falls back to 5173.

### Django Backend (Start Second, with VITE_PORT)

```python
# Start Django server, passing the Vite port from previous step
mcp__dev-manager__start(
    command="VITE_PORT=3011 uv run python3 manage.py runserver",
    cwd="/home/yxg/Workspace/django-dream-blog"
)
# Returns: { "status": "started", "port": 3010, "session_key": "B7K2" }
```

Django respects `PORT` env variable, falls back to 8000.
Django also needs `VITE_PORT` to know where to fetch frontend assets from.

**Important**: Use `uv run` to ensure the correct Python environment is used.

---

## Workflow

### Full Stack Development (Django + Vite)

1. **Start Vite first** - Try `pnpm dev`, fallback to `npm run dev` if pnpm fails
2. **Note the allocated port** from response (e.g., 3011)
3. **Start Django with VITE_PORT** set to Vite's port
   ```python
   mcp__dev-manager__start(
       command="VITE_PORT=<vite_port> uv run python3 manage.py runserver",
       ...
   )
   ```
4. **Run tests** against Django's allocated port
5. **Stop both servers** via `mcp__dev-manager__stop` (or wait for auto-cleanup)

### Backend Only

1. **Start Django** via `mcp__dev-manager__start(command="uv run python3 manage.py runserver", ...)`
2. **Run tests** against the allocated port
3. **Stop server** via `mcp__dev-manager__stop`

---

## Troubleshooting

**Daemon not running:**
- User must start daemon: `npx -y dev-manager-mcp`
- Check daemon is listening on default port 3009

**Port conflicts:**
- MCP daemon handles this automatically
- Servers receive unique ports starting at 3010

**pnpm not found error:**
- MCP daemon runs in its own environment, may not have pnpm in PATH
- **Solution**: Retry with `npm run dev` instead
- Both pnpm and npm work (package.json has both scripts configured)

**Server fails to start:**
- Use `mcp__dev-manager__tail(session_key)` to check logs
- Verify command and cwd are correct

---

## References

- [dev-manager-mcp GitHub](https://github.com/BloopAI/dev-manager-mcp)
- [dev-manager-mcp on npm](https://www.npmjs.com/package/dev-manager-mcp)
