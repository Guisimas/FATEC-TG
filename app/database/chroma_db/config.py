import chromadb
from chromadb.config import Settings

# ------------------------------------
# Conexao com banco de dados
# ------------------------------------


def connect_chroma():
    return chromadb.PersistentClient(
        path="./app/database/banco",
        settings=Settings(
            is_persistent=True,
            persist_directory=".app/database/banco",
            allow_reset=True,
            anonymized_telemetry=False),
    )
