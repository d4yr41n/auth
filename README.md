# Auth

React + Starlette: a basic auth implementation.

## Launch

### Server

```
cd auth/server
python -m venv .venv
. .env/bin/activate
pip install -r requirements.txt
uvicorn main:app
```

### Client

```
cd auth/client
npm i
npm run build
```

## Demo

![form](form.png)

![table](table.png)
