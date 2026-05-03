import uvicorn
import os

def run(args):
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = False

    for arg in args:
        if arg == "--reload":
            reload = True
        elif ":" in arg:
            host, port = arg.split(":")
            port = int(port)
        elif arg.isdigit():
            port = int(arg)
        else:
            host = arg

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload
    )