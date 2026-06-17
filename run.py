# ============================================================
# FILE: run.py
# TOOLS USED:
#   - uvicorn : ASGI server that runs your FastAPI app
# HOW TO USE:
#   Open terminal in the backend folder and run:
#   python run.py
# ============================================================

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)