from fastapi import FastAPI, Request
from schemas import JSONRPCRequest, JSONRPCResponse
from tools.web_summarizer import tool_metadata, run

app = FastAPI()

@app.post("/")
async def rpc_handler(request: Request):
    try:
        data = await request.json()
        req = JSONRPCRequest(**data)
    except Exception as e:
        return JSONRPCResponse(
            id=None,
            error={"code": -32700, "message": f"Parse error: {e}"}
        )

    if req.method == "tool.list":
        return JSONRPCResponse(id=req.id, result=[tool_metadata])

    elif req.method == "web_search_summarizer":
        if not req.params or "query" not in req.params:
            return JSONRPCResponse(
                id=req.id,
                error={"code": -32602, "message": "Missing required 'query' in params"}
            )
        try:
            result = run(req.params)
            return JSONRPCResponse(id=req.id, result=result)
        except Exception as e:
            return JSONRPCResponse(
                id=req.id,
                error={"code": -32000, "message": f"Internal error: {e}"}
            )

    return JSONRPCResponse(
        id=req.id,
        error={"code": -32601, "message": "Method not found"}
    )
