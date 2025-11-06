# 📈 Guida Rapida - Stock Data Downloader Automatico

## 🎯 Cosa fa questo progetto?

Questo sistema scarica automaticamente i dati di borsa per 1007 aziende (Russell 1000) ogni 2 giorni alle 2 di notte usando GitHub Actions. I dati vengono salvati e aggiornati automaticamente nel repository GitHub.

## 🚀 Setup Veloce (5 minuti)

### Passo 1: Crea un Repository su GitHub

1. Vai su [GitHub](https://github.com)
2. Clicca su **"New repository"** (o il pulsante +)
3. Dai un nome al repository (es: `stock-data-downloader`)
4. Scegli **Public** o **Private** (come preferisci)
5. **NON** aggiungere README, .gitignore o license (ce li abbiamo già)
6. Clicca **"Create repository"**
7. **Copia l'URL del repository** (es: `https://github.com/tuousername/stock-data-downloader.git`)

### Passo 2: Esegui lo Script di Setup

Apri PowerShell in questa cartella ed esegui:

```powershell
.\setup_github.ps1
```

Lo script ti chiederà l'URL del repository e farà tutto automaticamente:
- ✅ Inizializza Git
- ✅ Aggiunge tutti i file
- ✅ Crea il commit iniziale
- ✅ Fa il push su GitHub

### Passo 3: Abilita i Permessi di Scrittura per GitHub Actions

1. Vai sul tuo repository GitHub
2. Clicca su **Settings** (Impostazioni)
3. Nel menu laterale, clicca su **Actions** → **General**
4. Scorri fino a **"Workflow permissions"**
5. Seleziona **"Read and write permissions"**
6. Clicca **Save** (Salva)

### Passo 4: Fatto! 🎉

Il sistema è ora attivo e farà automaticamente:
- 📥 Download dei dati ogni 2 giorni alle 2:00 AM (UTC)
- 💾 Salvataggio dei dati in file compressi (.csv.gz)
- 🔄 Commit e push automatico dei nuovi dati
- 📝 Logging di tutte le operazioni

## 🎮 Come Usarlo

### Esecuzione Manuale

Puoi anche avviare il download manualmente:

1. Vai su GitHub → **Actions** tab
2. Clicca su **"Stock Data Downloader"**
3. Clicca **"Run workflow"**
4. Clicca **"Run workflow"** di nuovo per confermare

### Esecuzione Locale (per test)

```powershell
# Installa le dipendenze
pip install -r requirements.txt

# Esegui lo script
python stock_downloader.py
```

## 📊 Dove Sono i Dati?

I dati vengono salvati nella cartella `stock_data/`:
- Ogni file è un ticker (es: `AAPL.csv.gz` per Apple)
- Formato: CSV compresso con gzip
- Colonne: Datetime, Open, High, Low, Close, Volume, Ticker
- Intervallo: 30 minuti

### Come Leggere i Dati

```python
import pandas as pd

# Carica i dati di Apple
df = pd.read_csv('stock_data/AAPL.csv.gz', compression='gzip', parse_dates=['Datetime'])
print(df.head())
```

## ⚙️ Personalizzazione

### Cambiare la Frequenza

Modifica `.github/workflows/stock_downloader.yml`, riga con `cron:`:

```yaml
# Ogni giorno alle 2 AM
- cron: '0 2 * * *'

# Ogni 3 giorni alle 2 AM
- cron: '0 2 */3 * *'

# Ogni lunedì alle 2 AM
- cron: '0 2 * * 1'

# Due volte al giorno (2 AM e 2 PM)
- cron: '0 2,14 * * *'
```

### Cambiare l'Orario (Fuso Orario Italiano)

GitHub Actions usa UTC. Per avere le 2 di notte in Italia (UTC+1/+2):

```yaml
# 2 AM Italia = 1 AM UTC (ora solare) o 12 AM UTC (ora legale)
# Usa 1 AM UTC per essere sicuro:
- cron: '0 1 */2 * *'
```

### Cambiare il Periodo di Download

Modifica `stock_downloader.py`, riga ~262:

```python
# Default: scarica ultimi 3 giorni (da 2 giorni fa a oggi)
start_date = end_date - timedelta(days=2)

# Per scaricare l'ultima settimana:
start_date = end_date - timedelta(days=6)

# Per scaricare l'ultimo mese:
start_date = end_date - timedelta(days=29)
```

### Cambiare l'Intervallo dei Dati

Modifica `stock_downloader.py`, nelle chiamate a `download_all`:

```python
# Default: intervalli di 30 minuti
interval="30m"

# Opzioni disponibili:
interval="1m"   # 1 minuto (solo ultimi 7 giorni)
interval="5m"   # 5 minuti
interval="15m"  # 15 minuti
interval="1h"   # 1 ora
interval="1d"   # Giornaliero
interval="1wk"  # Settimanale
```

## 📋 Monitoraggio

### Vedere lo Stato

1. Vai su GitHub → **Actions**
2. Vedrai tutte le esecuzioni del workflow
3. ✅ Verde = successo
4. ❌ Rosso = errore
5. 🟡 Giallo = in esecuzione

### Log Dettagliati

- **Su GitHub**: Clicca su una esecuzione per vedere i log dettagliati
- **Nel repository**: Il file `download_log.txt` contiene lo storico completo

### Notifiche

GitHub ti invierà email se il workflow fallisce (puoi configurarlo nelle impostazioni).

## 🐛 Risoluzione Problemi

### Il Workflow Non Parte
- Controlla che GitHub Actions sia abilitato (Settings → Actions)
- Verifica la sintassi del cron
- I repository inattivi potrebbero avere i workflow disabilitati

### Errori di Permessi
- Vai su Settings → Actions → General
- Seleziona "Read and write permissions"
- Salva

### Download Falliti
- Controlla `download_log.txt`
- Alcuni ticker potrebbero non essere disponibili
- Yahoo Finance potrebbe avere limiti di rate

### Non Vedo i Dati
- Aspetta la prima esecuzione (ogni 2 giorni alle 2 AM)
- Oppure esegui manualmente (Actions → Run workflow)
- I file saranno in `stock_data/` dopo l'esecuzione

## 💡 Tips

1. **Backup**: GitHub conserva già tutto, ma puoi clonare il repo localmente
2. **Spazio**: Con 1007 ticker e dati compressi, aspettati ~100-500 MB
3. **Limiti GitHub**: Repository gratuiti hanno 1GB di spazio (più che sufficiente)
4. **Git LFS**: Se i file diventano troppo grandi, considera Git Large File Storage

## 📞 Supporto

- **GitHub Issues**: Apri un issue nel repository per problemi
- **GitHub Discussions**: Per domande e discussioni
- **Log**: Controlla sempre `download_log.txt` per errori dettagliati

## ✨ Funzionalità Extra

### Confronto Automatico
Il workflow crea automaticamente un sommario dopo ogni esecuzione con:
- Data e ora dell'esecuzione
- Numero di file scaricati
- Ultime voci del log
- Statistiche sui file

### Artifacts
Ogni esecuzione salva il log come "artifact" per 30 giorni, così puoi scaricarlo anche dopo.

### Intelligente
- **Deduplicazione**: Non scarica dati duplicati
- **Incrementale**: Aggiunge solo nuovi dati ai file esistenti
- **Rate Limiting**: Rispetta i limiti di Yahoo Finance
- **Error Handling**: Continua anche se alcuni ticker falliscono

## 🎓 Prossimi Passi

Una volta che il sistema funziona, puoi:
1. Aggiungere analisi automatiche dei dati
2. Creare visualizzazioni (grafici)
3. Implementare algoritmi di trading
4. Esportare dati in altri formati
5. Integrare con database
6. Creare API per accedere ai dati

## 📚 Risorse Utili

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Cron Syntax](https://crontab.guru/)
- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [Pandas Documentation](https://pandas.pydata.org/)

---

**Creato**: Novembre 2025  
**Piattaforma**: GitHub Actions  
**Linguaggio**: Python 3.11+  
**Licenza**: Open Source
