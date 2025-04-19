import pandas as pd

from pandas import DataFrame
from io import StringIO, BytesIO

from exceptions.DecodingException import DecodingException

def change_encoding_csv_xlsx(content: bytes, format: str = "csv") -> DataFrame:
    """
    Parses uploaded file content (CSV or XLSX) and returns it as a pandas DataFrame.

    Args:
        content (bytes): Raw file content as bytes.
        format (str, optional): File format - either "csv" or "xlsx". Defaults to "csv".

    Returns:
        DataFrame: Parsed data as a pandas DataFrame.

    Raises:
        UnicodeDecodeError: If CSV content is not valid UTF-8.
        ValueError: If unsupported format is provided.
    """
    try:
        if format == 'csv':
            df = pd.read_csv(StringIO(content.decode('utf-8')))
        else:
            df = pd.read_excel(BytesIO(content))
        return df
    except Exception as error:
        raise DecodingException(
            message = str(error)
        )