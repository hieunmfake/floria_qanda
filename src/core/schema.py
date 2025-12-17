from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Document(BaseModel):
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    # default_factory=dict đảm bảo mỗi instance nhận một đối tượng dict mới, tránh dùng chung tham chiếu.
    id: Optional[str] = None
    vector: Optional[List[float]] = None
