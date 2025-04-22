# INSTALILY MCP SERVER TEMPLATE

### Installation Instructions

First ensure that ```uv``` is installed:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Clone the repo:
```
git clone git@github.com:Instalily/instalily-mcp-server.git
cd instalily-mcp-server
```

Initialize the project with ```uv``` and install the packages required:
```
uv init project

uv add "mcp[cli]" starlette uvicorn anthropic
```

Create a ```.env``` file and add your anthropic key 
```
ANTHROPIC_API_KEY=...
```

### To Run

Not necessary each time but ensure you initialize packages properly:
```
source .venv/bin/activate
```

You will need two terminals from here. In the first, run the following:
```
uv run src/server.py  
```

Then in the second terminal run 
```
uv run mcp dev src/server.py
```

This opens a local development front end in your browser. Copy and paste the initialized link into Chrome and you can begin interacting with the tools, templates, and resources you create. On the left panel ensure that the connection endpoint is ```http://0.0.0.0:8080/sse```

Alternatively, for in-line development you can run:
```
uv run src/client.py http://0.0.0.0:8080/sse
```