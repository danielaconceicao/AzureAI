☁️ Architettura di Ricerca Basata su Azure AI</br>

Benvenuto in questo progetto che dimostra una pipeline completa per la creazione di una Base di Conoscenza (Knowledge Base) sfruttando i principali servizi di Azure AI e Storage.

Questo script illustra come analizzare un documento PDF, caricarlo su Blob Storage e indicizzarlo in Azure AI Search per renderlo ricercabile immediatamente.

🚀 Architettura del Progetto</br>
Il progetto collega tre servizi fondamentali di Azure in una sequenza automatizzata:

```
+----------------+       +-------------------+       +---------------+
| PDF Documento  |  -->  | Doc Intelligence  |  -->  | Azure AI Search|
+----------------+       |  (Estrazione Testo) |  -->  |  (Indicizzazione)   |
| (Buscofem.pdf) |       +-------------------+       +---------------+
                        |
                        +--> Azure Blob Storage
                             (Archiviazione)
```
🛠️ Funzionalità e Passaggi della Pipeline</br>
Questo script esegue i seguenti passaggi in sequenza:

1. **Estrazione del Testo (Azure AI Document Intelligence)** </br>
Il codice utilizza il modello prebuilt-read di Azure AI Document Intelligence per estrarre tutto il testo e le informazioni strutturate dal file PDF specificato.

* **Azione: Apre il file Buscofem.pdf e analizza il suo contenuto per ricavarne il testo completo.**

* **Risultato: Il testo estratto è aggregato in una singola stringa, pronto per l'indicizzazione.**

2. **Caricamento su Blob Storage**</br>
Il file PDF originale viene caricato nel contenitore di archiviazione configurato (pdfs).

* **Servizio: Azure Blob Storage.**

* **Azione: Stabilisce una connessione tramite storage_connection_string e carica il file Buscofem.pdf nel contenitore pdfs.**

3. **Creazione e Aggiornamento dell'Indice (Azure AI Search)**</br>
Questa sezione definisce lo schema dell'indice di ricerca e lo crea (o lo ignora se esiste già).

```Servizio: Azure AI Search.

Schema dell'Indice (kb-index):

id: Campo chiave univoco (stringa).

content: Campo ricercabile contenente il testo estratto dal PDF.
```

4. **Indicizzazione del Documento**</br>
Una volta creato l'indice, il testo estratto dal PDF (dalla Fase 1) viene inserito nell'indice come un documento ricercabile.

* **Azione: Il testo completo del PDF viene inviato all'indice kb-index con l'ID "1".**

* **Risultato: Il contenuto del PDF è ora disponibile per le query di ricerca full-text (ricerca per parole chiave).**

⚙️ **Configurazione e Prerequisiti**</br>
Per eseguire questo script, è essenziale configurare le credenziali di accesso ai servizi Azure.

Variabili d'Ambiente</br>
Tutte le credenziali sono caricate da un file .env tramite la libreria python-dotenv.

Variabile	Descrizione</br>
* DOC_INTELLIGENCE_KEY	Chiave API per Azure AI Document Intelligence.</br>
- DOC_INTELLIGENCE_ENDPOINT	URL dell'endpoint del servizio Document Intelligence.</br>
- STORAGE_CONNECTION_STRING	Stringa di connessione completa  l'account Azure Storage.</br>
- SEARCH_KEY	Chiave API per Azure AI Search.</br>
- SEARCH_ENDPOINT	URL dell'endpoint del servizio Azure AI Search.</br>

Esporta in Fogli
Dipendenze Python
Il progetto richiede l'installazione dei SDK ufficiali di Azure:


- azure-ai-formrecognizer
- azure-storage-blob
- azure-search-documents
- python-dotenv
- Puoi installarli con:



```
pip install -r requirements.txt
```

