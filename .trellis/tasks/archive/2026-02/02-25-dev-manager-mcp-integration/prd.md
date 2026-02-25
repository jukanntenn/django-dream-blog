# dev-manager-mcp Integration

## Goal

Integrate dev-manager-mcp into the project to enable AI agents to request dev servers via MCP, avoiding port conflicts across multiple projects. The MCP daemon manages server lifecycle and allocates ports via the `PORT` environment variable.

## What I Already Know

**dev-manager-mcp (from BloopAI):**
- MCP daemon that manages development servers
- Auto-allocates ports starting at 3010 (probes availability)
- MCP tools: `start`, `stop`, `status`, `tail`
- `start` takes `command` and optional `cwd`, returns `port` and `session_key`
- PORT is passed to the command via environment variable
- Auto-cleanup after 120s idle timeout
- Installation: `npx -y dev-manager-mcp` (daemon), MCP client config via stdio

**Current project setup:**
- **Django runserver**: `python manage.py runserver` → defaults to port 8000, no PORT env support
- **Vite dev server**: `pnpm dev` → defaults to port 5173, no explicit server config in vite.config.js
- **VSCode tasks**: "Start Django", "Start Vite", "Start All" - hardcoded commands

## Assumptions (to validate)

1. Both Django and Vite dev servers need to respect `PORT` environment variable
2. VSCode tasks should remain for manual use (no MCP integration needed there)
3. AI will use MCP tools when it needs to start servers for testing
4. Default ports (8000, 5173) should still work when PORT is not set

## Open Questions

None - requirements clarified.

## Requirements (evolving)

### Server Configuration
- [x] Django runserver respects `PORT` environment variable, fallback to 8000 (via manage.py)
- [x] Vite dev server respects `PORT` environment variable, fallback to 5173 (via vite.config.js)

### Documentation
- [ ] Add brief note in CLAUDE.md about MCP integration and PORT support
- [ ] Create `.trellis/spec/guides/dev-server-mcp.md` with MCP integration guidelines
- [ ] Update `.trellis/spec/guides/index.md` to include the new guide

## Acceptance Criteria (evolving)

- [ ] `PORT=3001 python manage.py runserver` starts Django on port 3001
- [ ] `PORT=3002 pnpm dev` starts Vite on port 3002
- [ ] AI documentation explains how to use dev-manager-mcp
- [ ] Default behavior unchanged when PORT is not set

## Definition of Done

- [ ] Django respects PORT env variable
- [ ] Vite PORT support documented (works out of box)
- [ ] CLAUDE.md updated with MCP note
- [ ] Trellis spec updated with MCP guidelines
- [ ] Manual testing: start servers with custom PORT

## Out of Scope (explicit)

- Changing VSCode tasks to use MCP (keep manual control)
- Automatic daemon startup (user responsibility)
- MCP server configuration file creation (user's global config)
- Detailed troubleshooting documentation

## Technical Notes

### Django Port Configuration

**Finding**: Django's runserver does NOT support PORT environment variable natively. Port is specified via:
1. Command line argument: `runserver 0.0.0.0:8000`
2. Default: `Command.default_port = '8000'`

**Implementation Options:**

**Option A: Modify manage.py (Recommended)**
Simple modification to read PORT env and inject into runserver command:
```python
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    # ... existing path setup ...

    # Support PORT environment variable for runserver
    if 'runserver' in sys.argv:
        # Check if port is already specified in command
        has_port_arg = any(':' in arg for arg in sys.argv)
        if not has_port_arg:
            port = os.environ.get('PORT', '8000')
            sys.argv.append(f'0.0.0.0:{port}')

    execute_from_command_line(sys.argv)
```
- **Pros**: Minimal change, works with MCP, backwards compatible
- **Cons**: Only affects runserver, not other commands

**Option B: Environment-based DEFAULT_PORT via custom Command**
Subclass runserver command to read PORT env. Overkill for this use case.

### Vite Port Configuration

**Finding**: Vite does NOT automatically read PORT environment variable. Need to configure `server.port` in vite.config.js:

```javascript
server: {
  port: Number(process.env.PORT) || 5173,
  host: "0.0.0.0",
}
```

**Implemented**: Added to `frontend/vite.config.js`

### Verified Behavior

```bash
# Vite - now works with vite.config.js change
PORT=3002 pnpm dev  # → starts on port 3002

# Django - works with manage.py modification
PORT=3001 uv run python3 manage.py runserver  # → starts on port 3001
```

### MCP Configuration Example

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

### MCP Tool Usage Example

```
// Start a dev server
mcp__dev-manager__start(command="python manage.py runserver", cwd="/path/to/project")
// Returns: { "status": "started", "port": 3010, "session_key": "A3X9" }

// Start Vite server
mcp__dev-manager__start(command="pnpm dev", cwd="/path/to/project/frontend")
// Returns: { "status": "started", "port": 3011, "session_key": "B7K2" }
```

### Files Modified

1. `manage.py` - Added PORT env support for runserver
2. `frontend/vite.config.js` - Added server.port reading from process.env.PORT
3. `config/settings/base.py` - Added VITE_PORT env support for django-vite
4. `CLAUDE.md` - Added brief MCP integration note with workflow
5. `.trellis/spec/guides/dev-server-mcp.md` - New dedicated guide for MCP integration
6. `.trellis/spec/guides/index.md` - Added reference to new guide

### Important: Workflow for Full Stack Testing

When using dev-manager-mcp for full stack testing:
1. Start Vite first → note allocated port (e.g., 3011)
2. Start Django with `VITE_PORT=3011` → Django fetches assets from correct Vite port
3. Run tests against Django's allocated port (e.g., 3010)
