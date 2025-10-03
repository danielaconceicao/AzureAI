from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchFieldDataType, SearchableField
)
from azure.search.documents import SearchClient
from dotenv import load_dotenv
import os

# conf
load_dotenv()
doc_intelligence_key = os.getenv("DOC_INTELLIGENCE_KEY")
doc_intelligence_endpoint = os.getenv("DOC_INTELLIGENCE_ENDPOINT")

storage_connection_string = os.getenv("STORAGE_CONNECTION_STRING")

search_key = os.getenv("SEARCH_KEY")
search_endpoint = os.getenv("SEARCH_ENDPOINT")

container_name = "pdfs"

index_name = "kb-index"

# extrair texto do pdf
document_analysis_client = DocumentAnalysisClient(
    endpoint=doc_intelligence_endpoint,
    credential=AzureKeyCredential(doc_intelligence_key)
)

with open("Buscofem.pdf", "rb") as f:
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-read", document=f)
    result = poller.result()

all_text = " ".join(
    [line.content for page in result.pages for line in page.lines])
print("Texto extraído:", all_text[:500], "...")

#  upload para blob storage
blob_service_client = BlobServiceClient.from_connection_string(
    storage_connection_string)
container_client = blob_service_client.get_container_client(container_name)

with open("Buscofem.pdf", "rb") as data:
    blob_client = container_client.get_blob_client("Buscofem.pdf")
    blob_client.upload_blob(data, overwrite=True)

print("PDF carregado no Blob Storage!")

#  criar índice no azure AI search
search_index_client = SearchIndexClient(
    search_endpoint, AzureKeyCredential(search_key))

fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="content", type=SearchFieldDataType.String)
]

index = SearchIndex(name=index_name, fields=fields)

# criar índice
try:
    search_index_client.create_index(index)
    print("indice criado!")
except Exception:
    print("indice já existe!") # <- se ja tiver um index nao quebre so me mande a msg

#  inserir documento no índice
search_client = SearchClient(
    search_endpoint, index_name, AzureKeyCredential(search_key))

doc = {"id": "1", "content": all_text} # <- inserimento
search_client.upload_documents([doc])

print("documento indexado")
