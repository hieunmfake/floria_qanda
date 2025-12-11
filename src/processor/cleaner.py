import re


def clean_transcript(raw_text: str) -> str:
    """Hàm làm sạch dữ liệu thô từ Youtube"""
    if not raw_text:
        return ""

    # 1: Xóa các thẻ nằm giữa ngoặc vuông [] hoặc ngoặc tròn ()
    text = re.sub(r"\[.*?\]", "", raw_text)
    text = re.sub(r"\(.*?\)", "", text)

    # 2: Xóa các kí tự xuống dòng để nối thành văn xuôi
    text = text.replace("\n", " ")

    # 3: Xóa các khoảng trắng thừa
    text = re.sub(r"\s+", " ", text)

    # 4: Xóa lặp từ đơn giản
    text = re.sub(r"\b(\w+)( \1\b)+", r"\1", text, flags=re.IGNORECASE)

    return text.strip()
