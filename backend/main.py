import sys
import argparse
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import uvicorn
from ai_memory_agent.config import settings
from ai_memory_agent.api.server import app
from demo.demo_story import run_full_demo
from demo.interactive_cli import main as run_interactive_cli


def main():
    parser = argparse.ArgumentParser(
        description="AI Security Operations & Compliance Memory Agent powered by Hindsight"
    )
    parser.add_argument(
        "mode",
        nargs="?",
        default="server",
        choices=["server", "demo", "cli"],
        help="Execution mode: 'server' (starts FastAPI backend), 'demo' (runs 10-step automated story), 'cli' (interactive terminal)",
    )
    parser.add_argument("--host", default=settings.HOST, help="Host address for FastAPI server")
    parser.add_argument("--port", type=int, default=settings.PORT, help="Port for FastAPI server")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")

    args = parser.parse_args()

    if args.mode == "demo":
        print("Running 10-Step Automated Demo Story...")
        run_full_demo()
    elif args.mode == "cli":
        print("Starting Interactive CLI...")
        run_interactive_cli()
    else:
        print(f"Starting {settings.APP_NAME} on http://{args.host}:{args.port}")
        print(f"Interactive Swagger UI: http://{args.host}:{args.port}/docs")
        uvicorn.run("ai_memory_agent.api.server:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
