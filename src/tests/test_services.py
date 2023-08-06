import io

import pytest
from ..services import get_pdf_text, compute_md5


def test_get_pdf_text_valid():
    # Classic paper on entropy by Claude Shannon (1948)"
    with open("tests/data/entropy.pdf", "rb") as f:
        pdf_content = f.read()

    # Using the get_pdf_text function to extract text
    extracted_text = get_pdf_text(pdf_content)

    # Assert that the text "Mathematical Theory" exists in the extracted text
    assert "Mathematical Theory" in extracted_text


def test_get_pdf_text_empty():
    # Given an empty PDF content as bytes
    pdf_content = b""

    # Using the get_pdf_text function to extract text
    with pytest.raises(Exception):  # Expecting an exception due to empty content
        get_pdf_text(pdf_content)


def test_get_pdf_text_invalid():
    # Given an invalid PDF content as bytes
    pdf_content = b"Not a valid PDF content"

    # Using the get_pdf_text function to extract text
    with pytest.raises(Exception):  # Expecting an exception due to invalid content
        get_pdf_text(pdf_content)


def test_compute_md5():
    # Create an in-memory binary stream with some data
    data = b"Hello, World!"
    file_object = io.BytesIO(data)

    # Compute its MD5 hash
    result = compute_md5(file_object)

    # Known MD5 hash for the string "Hello, World!"
    expected = "65a8e27d8879283831b664bd8b7f0ad4"

    assert result == expected
