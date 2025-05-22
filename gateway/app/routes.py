from fastapi import APIRouter, Depends, Request, Response, UploadFile, File, HTTPException
from .dependencies import verify_token
from common.config import settings
import httpx

router = APIRouter(prefix="/api")

FILE_SERVICE_URL = f"http://file_service:8001"
ANALYSIS_SERVICE_URL = f"http://analysis_service:8002"

async_client = httpx.AsyncClient(timeout=10.0)

# @router.api_route("/files/{path:path}", methods=["GET", "POST"])
# async def proxy_files(path: str, request: Request, payload: dict = Depends(verify_token)):
#     if request.method == "GET":
#         url = f"{FILE_SERVICE_URL}/files/{path}"
#         headers = {k: v for k, v in request.headers.items() if k.lower() == "authorization"}
#         resp = await async_client.get(url, headers=headers)
#     else:
#         url = f"{FILE_SERVICE_URL}/files/"
#         body = await request.body()
#         headers = {k: v for k, v in request.headers.items() if k.lower() in ("authorization", "content-type")}
#         resp = await async_client.post(url, headers=headers, content=body)
#     return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)


@router.post("/files/", summary="Upload file")
async def upload_file(
    file: UploadFile = File(...),
    token: dict = Depends(verify_token)
):
    url = f"{FILE_SERVICE_URL}/files/"
    headers = {"Authorization": f"Bearer {token['sub']}"}
    files = {"file": (file.filename, await file.read(), file.content_type)}

    resp = await async_client.post(url, headers=headers, files=files)
    return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)

@router.get("/files/{file_id}", summary="Download file by ID")
async def download_file(
    file_id: int,
    token: dict = Depends(verify_token)
):
    url = f"{FILE_SERVICE_URL}/files/{file_id}"
    headers = {"Authorization": f"Bearer {token['sub']}"}

    resp = await async_client.get(url, headers=headers)

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=resp.headers
    )

@router.api_route("/analyze/{file_id}", methods=["GET", "POST"])
async def proxy_analyze(file_id: str, request: Request, payload: dict = Depends(verify_token)):
    url = f"{ANALYSIS_SERVICE_URL}/analyze/{file_id}"
    headers = {k: v for k, v in request.headers.items() if k.lower() == "authorization"}
    if request.method == "GET":
        resp = await async_client.get(url, headers=headers)
    else:
        resp = await async_client.post(url, headers=headers)
    return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)

@router.get("/analyze/{file_id}/wordcloud", summary="Download wordcloud image")
async def proxy_wordcloud(
    file_id: int,
    token: dict = Depends(verify_token)
):
    url = f"{ANALYSIS_SERVICE_URL}/analyze/{file_id}/wordcloud"
    headers = {"Authorization": f"Bearer {token['sub']}"}

    resp = await async_client.get(url, headers=headers)
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=resp.headers,
        media_type=resp.headers.get("content-type", "application/octet-stream")
    )