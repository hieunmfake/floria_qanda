from abc import ABC, abstractmethod
from typing import List

from src.core.schema import Document


class BaseVectorStore(ABC):

    @abstractmethod
    def connect(self):
        """Create connection to VectorDB"""
        pass

    @abstractmethod
    def add_documents(self, documents: List[Document]) -> bool:
        """
        Save documents list into VectorDB
        """
        pass

    @abstractmethod
    def search_similarity(
        self, query_vector: List[float], k: int = 5
    ) -> List[Document]:
        """
        Performs a similarity search.
        Args:
            query_vectors: The query vectors to search for.
            k: The number of top similar Documents to return.
        Returns:
            A list of the top k documents with the highest similarity.
        """
        pass

    @abstractmethod
    def delete(self, doc_ids: List[str]) -> bool:
        """
        Delete documents by a list of their IDs.
        """
        pass
