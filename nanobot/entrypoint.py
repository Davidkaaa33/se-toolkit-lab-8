import json, os, shutil
from pathlib import Path

CONFIG_PATH = Path("/app/nanobot/config.json")
RESOLVED_PATH = Path("/tmp/config.resolved.json")
IMAGE_WORKSPACE = Path("/app/nanobot/workspace")
RUNTIME_WORKSPACE = Path("/tmp/nanobot-workspace")
VENV_PYTHON = "/app/.venv/bin/python"

def set_path(d, path, value):
    cur = d
    for k in path[:-1]:
        cur = cur.setdefault(k, {})
    cur[path[-1]] = value

def req(name):
    v = os.getenv(name, "").strip()
    if not v:
        raise RuntimeError(f"Missing required env var: {name}")
    return v

if not RUNTIME_WORKSPACE.exists():
    shutil.copytree(IMAGE_WORKSPACE, RUNTIME_WORKSPACE)
RUNTIME_WORKSPACE.mkdir(parents=True, exist_ok=True)

cfg = json.loads(CONFIG_PATH.read_text())
set_path(cfg, ["providers","custom","apiKey"], req("LLM_API_KEY"))
set_path(cfg, ["providers","custom","apiBase"], req("LLM_API_BASE_URL"))
set_path(cfg, ["agents","defaults","model"], req("LLM_API_MODEL"))
set_path(cfg, ["gateway","host"], req("NANOBOT_GATEWAY_CONTAINER_ADDRESS"))
set_path(cfg, ["gateway","port"], int(req("NANOBOT_GATEWAY_CONTAINER_PORT")))

set_path(cfg, ["channels","webchat","enabled"], True)
set_path(cfg, ["channels","webchat","host"], req("NANOBOT_WEBCHAT_CONTAINER_ADDRESS"))
set_path(cfg, ["channels","webchat","port"], int(req("NANOBOT_WEBCHAT_CONTAINER_PORT")))
set_path(cfg, ["channels","webchat","allowFrom"], ["*"])

set_path(cfg, ["tools","mcpServers","lms","command"], VENV_PYTHON)
set_path(cfg, ["tools","mcpServers","lms","args"], ["-m","mcp_lms"])
set_path(cfg, ["tools","mcpServers","lms","env"], {
    "NANOBOT_LMS_BACKEND_URL": req("NANOBOT_LMS_BACKEND_URL"),
    "NANOBOT_LMS_API_KEY": req("NANOBOT_LMS_API_KEY"),
})

set_path(cfg, ["tools","mcpServers","webchat","command"], VENV_PYTHON)
set_path(cfg, ["tools","mcpServers","webchat","args"], ["-m","mcp_webchat"])
set_path(cfg, ["tools","mcpServers","webchat","env"], {
    "NANOBOT_UI_RELAY_URL": os.getenv("NANOBOT_UI_RELAY_URL", "http://127.0.0.1:8766"),
    "NANOBOT_UI_RELAY_TOKEN": os.getenv("NANOBOT_UI_RELAY_TOKEN", req("NANOBOT_ACCESS_KEY")),
})

set_path(cfg, ["tools","mcpServers","obs","command"], VENV_PYTHON)
set_path(cfg, ["tools","mcpServers","obs","args"], ["-m","mcp_obs"])
set_path(cfg, ["tools","mcpServers","obs","env"], {
    "NANOBOT_VICTORIALOGS_URL": req("NANOBOT_VICTORIALOGS_URL"),
    "NANOBOT_VICTORIATRACES_URL": req("NANOBOT_VICTORIATRACES_URL"),
})

RESOLVED_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2))

os.execv(VENV_PYTHON, [
    VENV_PYTHON, "-m", "nanobot", "gateway",
    "--config", str(RESOLVED_PATH),
    "--workspace", str(RUNTIME_WORKSPACE),
])
