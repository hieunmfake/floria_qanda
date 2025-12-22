from typing import List

from loguru import logger
from qdrant_client import QdrantClient, models

from src.core.schema import Document
from src.storage.base import BaseVectorStore


class QdrantStore(BaseVectorStore):
    def __init__(
        self,
        url: str,
        api_key: str,
        collection_name: str,
        vector_size: int,
        batch_size: int = 100,
    ):
        """
        Initialize Qdrant store.

        Args:
            url (str): Qdrant URL.
            api_key (str): Qdrant API key.
            collection_name (str): Qdrant collection name.
            vector_size (int): Vector size.
            batch_size (int): Batch size for upsert.
        """

        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.batch_size = batch_size

    def connect(self):
        """
        Connect to Qdrant.
        """
        if not self.client.collection_exists(collection_name=self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size, distance=models.Distance.COSINE
                ),
            )

        return self.client

    def add_documents(self, documents: List[Document]) -> bool:
        """
        Add documents to Qdrant.

        Args:
            documents (List[Document]): List of documents to add.

        Returns:
            bool: True if documents are added successfully, False otherwise.
        """
        try:
            for i in range(0, len(documents), self.batch_size):
                points: List[models.PointStruct] = []
                batch = documents[i : i + self.batch_size]
                for doc in batch:
                    points.append(
                        models.PointStruct(
                            id=doc.id,
                            vector=doc.vector,
                            payload={"content": doc.content, **doc.metadata},
                        )
                    )

                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points,
                )

            return True
        except Exception as e:
            logger.error(f"Error adding documents to Qdrant: {e}")
            return False

    def search_similarity(
        self, query_vector: List[float], k: int = 5
    ) -> List[Document]:
        """
        Search for similar documents in Qdrant.

        Args:
            query_vector (List[float]): Query vector.
            k (int): Number of similar documents to return.

        Returns:
            List[Document]: List of similar documents.
        """
        try:
            result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=k,
            )
            if result:
                return [
                    Document(
                        id=r.id,
                        content=r.payload["content"],
                        vector=r.vector,
                        metadata={k: v for k, v in r.payload.items() if k != "content"},
                    )
                    for r in result
                ]

            return []
        except Exception as e:
            logger.error(f"Error searching documents in Qdrant: {e}")
            return []

    def delete(self, doc_ids: List[str]) -> bool:
        """
        Delete documents from Qdrant.

        Args:
            doc_ids (List[str]): List of document IDs to delete.

        Returns:
            bool: True if documents are deleted successfully, False otherwise.
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(ids=doc_ids),
            )
            return True
        except Exception as e:
            logger.error(f"Error deleting documents from Qdrant: {e}")
            return False
