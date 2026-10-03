# Condivisione sui social

Prepara la condivisione di un post su LinkedIn, Facebook e Threads, senza API e senza token da rinnovare: lo script copia il testo negli appunti e apre la finestra di condivisione di ogni social, una alla volta. La pubblicazione resta manuale.

```
python tools/social/share.py                     # post più recente in italiano
python tools/social/share.py --lang en           # post più recente in inglese
python tools/social/share.py _posts/it/2026-10-03-....md
python tools/social/share.py --only linkedin,threads
```

Serve PyYAML (`pip install pyyaml`), come per il CV.

| Social | Cosa arriva già compilato |
|---|---|
| LinkedIn | testo e link |
| Threads | testo e link (massimo 500 caratteri in tutto) |
| Facebook | solo il link: il testo si incolla dagli appunti |

## Il testo

Si scrive nel front matter del post, a mano:

```yaml
social: "Un testo per tutti i social"
```

oppure uno diverso per social; quelli che mancano usano `default`:

```yaml
social:
  default: "Testo per LinkedIn e Facebook"
  threads: "Versione corta per Threads"
```

Senza `social:` lo script usa `intro`. Il link al post lo aggiunge lui.

## Prima che il post sia online, no

Lo script controlla che l'indirizzo del post risponda e si ferma se non risponde ancora: LinkedIn e Facebook tengono in cache l'anteprima di un link, e un link condiviso prima del deploy resta per giorni con un 404 o senza immagine. `--force` salta il controllo. I post con data futura non vengono scelti come "più recente" finché non arriva il loro giorno.

Il link di LinkedIn con il testo precompilato (`feed/?shareActive=true&text=`) non è documentato ufficialmente: se un giorno smette di funzionare, il testo è comunque negli appunti.
