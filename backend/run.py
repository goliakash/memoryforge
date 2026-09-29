import sys
import subprocess
from pathlib import Path

# Ensure UTF-8 stdout on Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Ensure required dependencies are present
try:
    import uvicorn
    import fastapi
except ImportError:
    print("[Launcher] Dependencies missing. Installing backend/requirements.txt...")
    req_file = BASE_DIR / "requirements.txt"
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_file)])
        import uvicorn
    except Exception as e:
        print(f"❌ Error installing dependencies automatically: {e}")
        print("Please run: pip3 install -r backend/requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 65)
    print("🧠 MEMORY FORGE: SEC-OPS & COMPLIANCE MEMORY AGENT")
    print("🛡️ Turning Incidents into Persistent Organizational Memory")
    print("🚀 Server starting at: http://localhost:8000")
    print("📖 API Swagger docs at: http://localhost:8000/docs")
    print("=" * 65)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

