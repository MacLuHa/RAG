from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from docx import Document
from io import BytesIO

from utils.change_encoding import change_encoding_csv_xlsx
from exceptions.ServerException import ServerException

document_router = APIRouter(
    prefix="/document"
)

@document_router.post("")
@document_router.post("/")
async def get_document(document: UploadFile = File(...)):
    """
    Обрабатывает загруженный документ (.docx, .txt, .csv, .xlsx) и возвращает его содержимое в виде JSON-ответа.

    Поддерживаются следующие форматы:
    - `.docx` — извлекает текст из абзацев с помощью библиотеки `python-docx`.
    - `.txt` — декодирует содержимое как UTF-8 строку.
    - `.csv` / `.xlsx` — парсит в DataFrame с помощью `pandas`, возвращает список строк в виде словарей.

    Args:
        document (UploadFile): Загруженный файл. Поддерживаемые расширения: `.docx`, `.txt`, `.csv`, `.xlsx`.

    Returns:
        JSONResponse:
            {
                "text": [...]  # список строк или словарей в зависимости от формата
            }

    Raises:
        ServerException: При ошибке чтения файла или парсинга данных.

    Примечания:
        - `.csv` читается с предположением кодировки UTF-8.
        - Функция `change_encoding_csv_xlsx` должна корректно обрабатывать переданный формат.
        - При использовании нестандартной кодировки в `.csv` может потребоваться автоопределение через chardet.
    """
    try:
        if document.filename.endswith(".docx"):
            content = await document.read()
            doc = Document(BytesIO(content))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return JSONResponse(
                status_code=200,
                content={
                    "text": paragraphs
                }
            )
        elif document.filename.endswith(".txt"):
            content = await document.read()
            return JSONResponse(
                status_code=200,
                content={
                    "text": str(content.decode())
                }
            )
        elif document.filename.endswith(('.csv','.xlsx')):
            content = await document.read()
            table = change_encoding_csv_xlsx(
                content,
                format=document.filename.split('.')[-1]
            )
            print(document.filename.split('.')[-1])
            return JSONResponse(
                status_code=200,
                content={
                    "text": str(table.to_dict(orient="records"))
                }
            )
    except Exception as error:
        raise ServerException(
            message = str(error)
        )
