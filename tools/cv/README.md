# CV in PDF

Genera il CV in PDF dai dati del sito, in due versioni:

| Versione | Dati personali | Output |
|---|---|---|
| Pubblica (scaricabile dal sito) | solo città | `static/assets/cv/CV_Cristian_Castellari.pdf` |
| Recruiter | indirizzo, telefono, data di nascita, consenso privacy | `static/assets/cv/CV_Cristian_Castellari_completo.pdf` (ignorato da git) |

```
python tools/cv/build.py
```

Serve PyYAML (`pip install pyyaml`) e Microsoft Edge, che stampa l'HTML in PDF.

## Da dove arrivano i contenuti

- **Esperienze e competenze**: `_data/index/careers.yml` e `skills.yml`, gli stessi del sito (testi in italiano). Aggiornando il sito si aggiorna anche il CV: basta rilanciare lo script. Nel PDF le competenze sono etichette senza percentuale, e i ruoli più vecchi usano descrizioni più brevi (`career_desc` in `cv.yml`).
- **Profilo, numeri chiave, contatti pubblici, lingue, certificazioni, corsi, progetti principali e progetti personali**: `tools/cv/cv.yml`. Certificazioni e corsi sono allineati a LinkedIn (settembre 2026); le certificazioni scadute sono omesse, l'elenco è nel commento del file.
- **Dati personali della versione recruiter**: `tools/cv/private.yml`. È in `.gitignore` e **non va committato**: il repository è pubblico. Lo stesso vale per il PDF recruiter, che finisce accanto a quello pubblico solo per comodità. Se manca, lo script genera solo la versione pubblica. Formato:

```yaml
address:
  - Via Esempio 1
  - 40026 Imola (BO)
phone: 000 0000000
birth_date: 01-01-1970
privacy: >-
  Autorizzo il trattamento dei dati personali ...
```

## Stile

Il CV deve stare in **2 pagine**: dopo ogni modifica controlla il numero di pagine dei PDF generati. Se sfora, accorcia i testi in `cv.yml`. Il consenso privacy della versione recruiter è posizionato in fondo alla colonna blu di pagina 2, quindi presuppone proprio 2 pagine.


`cv.css`, formato A4, font Source Sans Pro in `fonts/` (SIL Open Font License, vedi `fonts/OFL.txt`). I file HTML intermedi restano in `tools/cv/out/` e si possono aprire nel browser per controllare il layout.
