from fastapi import Header, HTTPException

async def get_token_header(x_token: str = Header(...)):
    pass 