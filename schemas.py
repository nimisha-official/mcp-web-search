from pydantic import BaseModel
from typing import Optional, Any, Dict

class JSONRPCRequest(BaseModel):
    jsonrpc: str
    method: str
    params: Optional[dict]
    id: Optional[str]

class JSONRPCResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[str]

class ToolMetadata(BaseModel):
    name: str
    description: str
    parameters: dict
