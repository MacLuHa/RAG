from fastapi import UploadFile, File, HTTPException, Depends
from io import BytesIO

from utils.check_file_extension_dev import check_file_extension_dev

MAX_FILE_SIZE = 10 * 1024 * 1024

async def check_size_file_dev(document: UploadFile = Depends(check_file_extension_dev)) -> UploadFile:
    content = await document.read()
    if len(content)> MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="The file size must not exceed 10 MB"
        )
    document.file = BytesIO(content)
    return document