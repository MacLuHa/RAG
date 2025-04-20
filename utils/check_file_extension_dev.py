from fastapi import UploadFile, File, HTTPException

def check_file_extension_dev(document: UploadFile = File(...)) -> UploadFile:
    if not document.filename.endswith(('.csv', '.xlsx', '.docx', '.txt')):
        raise HTTPException(
            status_code=400,
            detail=f'Extension {document.filename.split('.')[-1]} is not supported. Supported extensions - xlsx, csv, docx, txt.'
        )
    return document