from fastmcp import FastMCP
from pathlib import Path

app = FastMCP("fastmcp-server")

# Controlled sandbox directory
SANDBOX = Path("sandbox").resolve()
SANDBOX.mkdir(exist_ok=True)

def safe_path(filename: str) -> Path:
    path = (SANDBOX / filename).resolve()
    if SANDBOX not in path.parents and path != SANDBOX:
        raise ValueError("Access denied")
    return path

@app.tool()
def list_files() -> list[str]:
    """List all files in sandbox"""
    return [p.name for p in SANDBOX.iterdir() if p.is_file()]

@app.tool()
def read_file(filename: str) -> str:
    """Read a file inside sandbox safely"""
    try:
        file_path = safe_path(filename)
    except ValueError:
        return "Access denied"

    if not file_path.exists():
        return "File not found"

    return file_path.read_text(encoding="utf-8")

@app.tool()
def write_file(filename: str, content: str) -> str:
    """Write file inside sandbox safely"""
    try:
        file_path = safe_path(filename)
    except ValueError:
        return "Access denied"

    file_path.write_text(content, encoding="utf-8")
    return "Written successfully"

if __name__ == "__main__":
    app.run()
