# Status del Sistema

## 📊 Informazioni di Sistema

**Ultimo Aggiornamento**: Automatico ad ogni esecuzione  
**Frequenza**: Ogni 2 giorni alle 2:00 AM UTC  
**Tickers Monitorati**: 1007 (Russell 1000)  
**Intervallo Dati**: 30 minuti  
**Periodo**: Ultimi 3 giorni  

## 🔄 Stato Workflow

Dopo aver configurato il repository, aggiungi questo badge al README:

```markdown
![Stock Downloader](https://github.com/USERNAME/REPO_NAME/actions/workflows/stock_downloader.yml/badge.svg)
```

Sostituisci `USERNAME` e `REPO_NAME` con i tuoi valori.

## 📈 Statistiche

Queste vengono aggiornate automaticamente dopo ogni esecuzione e sono visibili nella sezione "Summary" di ogni workflow run.

## 🔍 Come Verificare

1. Vai su **Actions** tab nel tuo repository
2. Clicca sull'ultima esecuzione di "Stock Data Downloader"
3. Guarda la sezione **Summary** per vedere:
   - Numero di file scaricati
   - Tempo di esecuzione
   - Errori eventuali
   - Ultimi log

## 📝 Log

Il file `download_log.txt` viene aggiornato ad ogni esecuzione e contiene:
- Timestamp di ogni operazione
- Successi e fallimenti per ticker
- Errori dettagliati
- Statistiche finali

## 🚨 Avvisi

Se il workflow fallisce, GitHub ti invierà una notifica email (se hai abilitato le notifiche).

Puoi controllare manualmente lo stato in qualsiasi momento dalla tab **Actions**.
