import uvicorn

def run(args):
    host = "127.0.0.1"
    port = 8000
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
        reload=reload,
    )