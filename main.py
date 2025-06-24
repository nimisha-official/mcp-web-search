from fastapi import FastAPI, Request
from schemas import JSONRPCRequest, JSONRPCResponse
from tools.web_summarizer import tool_metadata, run

app = FastAPI()

@app.post("/")
async def rpc_handler(request: Request):
    data = await request.json()
    req = JSONRPCRequest(**data)

    if req.method == "tool.list":
        return JSONRPCResponse(id=req.id, result=[tool_metadata])

    if req.method == "web_search_summarizer":
        result = run(req.params)
        return JSONRPCResponse(id=req.id, result=result)

    return JSONRPCResponse(id=req.id, error={"code": -32601, "message": "Method not found"})