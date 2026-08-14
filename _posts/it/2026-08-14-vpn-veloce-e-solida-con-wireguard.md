---
title: "Una VPN veloce e solida con WireGuard: da Windows Server 2022 a Windows 11"
layout: post
date: '2026-08-14 00:15:00'
description: "Guida pratica a una VPN WireGuard con server su Windows Server 2022 e client Windows 11: chiavi, configurazione, port forwarding, tunnel completo o split, e sicurezza."
intro: "WireGuard non ha bisogno di grandi presentazioni: codice minuscolo, crittografia moderna, prestazioni che con OpenVPN e IPsec te le sogni. Quello che manca in giro è una guida che parta da un caso concreto e frequente — server su Windows Server 2022, client su Windows 11 — senza dare per scontati passaggi che su Windows non sono ovvi come su Linux."
image: "/static/assets/img/blog/wireguard-windows/cover.png"
image_dark: "/static/assets/img/blog/wireguard-windows/cover-dark.png"
lang: it_IT
categories:
- Infrastruttura & Sistemi
keywords: wireguard, vpn, windows server 2022, windows 11, networking, sicurezza, tunnel, powershell, nat
tags:
- windows-server
- windows11
- vpn
- wireguard
- networking
- sicurezza
permalink: "/it/blog/infrastruttura/:title/"
redirect_from: "/blog/infrastruttura/vpn-veloce-e-solida-con-wireguard/"
translation_key: wireguard-windows-server-2022-vpn
icon: fa-lock
---
Sono certificato Fortinet NSE6 e le VPN le so costruire, ma quando serve qualcosa di pronto in pochi click — comprese le VPN onboard sui router Mikrotik, magari per raggiungere l'intera rete di un cliente — uso **WireGuard**: meno configurazione, meno cose che si rompono, e una velocità che OpenVPN e IPsec non riescono ad avvicinare. Il protocollo è nato su Linux, ma il client ufficiale per Windows è maturo da tempo, e da quando esiste il driver **WireGuardNT** (a livello kernel, non più il vecchio `wireguard-go` in user space) le prestazioni su Windows sono del tutto in linea con quelle su Linux.

In questo articolo mettiamo in piedi uno scenario molto comune: un **server WireGuard su Windows Server 2022** che fa da punto d'ingresso per uno o più **client Windows 11**, con accesso alla rete locale dell'ufficio e, opzionalmente, un tunnel completo per instradare anche il traffico Internet. Userò nomi ed indirizzi IP generici — sostituiteli con i vostri prima di andare in produzione.

* TOC
{:toc}

## Perché WireGuard e non OpenVPN o IPsec

Qualche numero e qualche motivo concreto, senza dilungarmi troppo:

- **Codice minuscolo**: il core di WireGuard è poche migliaia di righe, contro le centinaia di migliaia di OpenVPN. Meno codice vuol dire meno superficie d'attacco e una revisione di sicurezza molto più semplice.
- **Crittografia moderna e non negoziabile**: Curve25519, ChaCha20-Poly1305, BLAKE2s. Non ci sono liste di cifrari da configurare né vecchi algoritmi da disabilitare a mano: WireGuard usa una sola suite crittografica, aggiornata, punto.
- **Solo UDP**: niente "TCP-over-TCP meltdown" (il rallentamento tipico di OpenVPN in modalità TCP su reti con perdita di pacchetti).
- **Roaming istantaneo**: un client può cambiare rete — dal Wi-Fi di casa al 5G, da un hotel a un altro — senza rinegoziare il tunnel. Il server si accorge del nuovo IP sorgente al primo pacchetto valido e continua da lì.
- **Nessuna sessione, nessuno stato lato server** finché non arriva traffico: il server non tiene processi appesi per ogni client connesso.

Il rovescio della medaglia: WireGuard **non ha un concetto di utente/password**. L'identità di un peer è la sua chiave pubblica, punto. Se vi serve un'autenticazione utente-per-utente in stile "aziendale", va costruita sopra (una coppia di chiavi per persona/dispositivo, mai condivisa) — ne parlo più avanti nella sezione sulla sicurezza.

## Prerequisiti

- Un **Windows Server 2022** con un indirizzo IP pubblico, oppure dietro un router su cui potete fare port forwarding.
- Uno o più **Windows 11** da collegare in VPN.
- Il client ufficiale **WireGuard per Windows**, stesso installer su server e client (link nella sezione [Download](#download)).
- Accesso amministrativo su entrambe le macchine, e la possibilità di aprire una porta UDP sul firewall (e sul router, se il server è dietro NAT).
- Se volete che i client raggiungano anche la LAN dell'ufficio (non solo il server), un minimo di pianificazione degli indirizzi: vedi lo schema qui sotto.

## Architettura e schema di indirizzamento

Lo scenario che useremo come riferimento in tutto l'articolo:

![Schema: client Windows 11, tunnel WireGuard cifrato attraverso Internet e un router con NAT/port-forward sulla porta UDP 51820, fino al server Windows Server 2022, che espone anche la LAN dell'ufficio 192.168.1.0/24](/static/assets/img/blog/wireguard-windows/diagram-topology.png)

- Rete WireGuard: **10.66.0.0/24** (una sottorete dedicata alla VPN, separata dalla LAN reale — così evitiamo conflitti di routing).
- Server: indirizzo VPN `10.66.0.1`, indirizzo LAN `192.168.1.10`.
- Client: `10.66.0.2`, `10.66.0.3`, ecc. — un indirizzo per dispositivo.
- Porta di ascolto: **UDP 51820** (quella di default; potete cambiarla, vedi la sezione sicurezza).
- LAN dell'ufficio da raggiungere in VPN: `192.168.1.0/24`.

> **Nota:** se il server è dietro un router (es. connessione domestica o in un ufficio senza IP pubblico diretto), serve un **port forward UDP 51820 → indirizzo LAN del server**. Se l'IP pubblico non è statico, aggiungete un servizio di DDNS (Dynamic DNS) e usate l'hostname invece dell'IP nell'`Endpoint` del client.

## Installazione su Windows Server 2022

Installate [WireGuard per Windows](https://www.wireguard.com/install/){:target="_blank"} con l'MSI ufficiale (stesso installer del client). L'app si apre con un pannello di gestione tunnel: la useremo solo per generare le chiavi la prima volta, perché su un server la modalità corretta è avviarlo **come servizio Windows**, non lasciarlo agganciato a una sessione utente.

### Generare la coppia di chiavi del server

Dal pannello **Gestisci tunnel** dell'app, scegliete **Aggiungi tunnel > Aggiungi tunnel vuoto**: viene generata subito una nuova coppia di chiavi, con la chiave privata già inserita nell'editor di configurazione e la chiave pubblica corrispondente visibile nel pannello di dettaglio del tunnel. Copiatevi da qualche parte la chiave pubblica: dovrete inserirla nella configurazione di ogni client.

> **Attenzione:** la chiave privata è l'unica cosa che identifica il server (o un client) nella VPN — trattatela come una password. Non giriatela per email o chat, non mettetela in un repository, e se sospettate che sia stata esposta rigeneratela e aggiornate tutti i peer.

### Il file di configurazione del server

Sostituite il contenuto dell'editor con qualcosa di questo tipo (adattando indirizzi e chiavi):

```ini
[Interface]
PrivateKey = <chiave privata del server>
Address = 10.66.0.1/24
ListenPort = 51820

[Peer]
# laptop-01
PublicKey = <chiave pubblica del client>
AllowedIPs = 10.66.0.2/32
```

Ogni client ha il suo blocco `[Peer]`, con la propria chiave pubblica e un solo indirizzo `/32` (il suo, non l'intera sottorete: è così che WireGuard sa a quale peer instradare i pacchetti diretti a quell'IP). Salvate il file come `C:\WireGuard\wg0.conf`.

### Attivare il tunnel come servizio Windows

Su un server, evitate di usare il pulsante "Attiva" dell'app grafica: quel tunnel resta legato alla sessione dell'utente che l'ha avviato e si ferma al logout. La via corretta è installarlo come **servizio**, così parte da solo al boot ed è indipendente da qualunque sessione:

```powershell
& "C:\Program Files\WireGuard\wireguard.exe" /installtunnelservice C:\WireGuard\wg0.conf
```

Per fermarlo o rimuoverlo in seguito:

```powershell
& "C:\Program Files\WireGuard\wireguard.exe" /uninstalltunnelservice wg0
```

Verificate che il servizio sia attivo con `Get-Service WireGuardTunnel*`.

### Aprire la porta sul firewall e sul router

Sul firewall di Windows:

```powershell
New-NetFirewallRule -DisplayName "WireGuard VPN" -Direction Inbound -Protocol UDP -LocalPort 51820 -Action Allow
```

Se il server è dietro un router, aggiungete anche lì il port forward UDP 51820 verso l'indirizzo LAN del server (`192.168.1.10` nel nostro schema).

## Configurazione del client Windows 11

### Generare la coppia di chiavi del client

Stessa procedura vista per il server: installate [WireGuard per Windows](https://www.wireguard.com/install/){:target="_blank"}, **Aggiungi tunnel > Aggiungi tunnel vuoto**, copiate la chiave pubblica generata (vi servirà per il blocco `[Peer]` sul server).

### Il file di configurazione del client

```ini
[Interface]
PrivateKey = <chiave privata del client>
Address = 10.66.0.2/24
DNS = 192.168.1.1

[Peer]
PublicKey = <chiave pubblica del server>
Endpoint = vpn.tuodominio.it:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

Un paio di campi meritano una spiegazione:

- **`Endpoint`**: l'indirizzo pubblico (o l'hostname DDNS) e la porta a cui il client si connette. È l'unico posto dove serve un indirizzo "raggiungibile dall'esterno" — il server non ha bisogno di conoscere l'IP del client in anticipo.
- **`PersistentKeepalive = 25`**: manda un pacchetto vuoto ogni 25 secondi per tenere aperto il mapping NAT del router del client. Senza, se il client è dietro un NAT (quasi sempre, su reti domestiche o mobili), il tunnel può "addormentarsi" e il server non riesce più a raggiungerlo per primo.
- **`AllowedIPs`**: qui decidete se fare tunnel completo o split tunnel — se ne parla nella prossima sezione.

Importate il file da **WireGuard > Importa tunnel da file...**, oppure incollate il contenuto direttamente nell'editor del tunnel vuoto creato prima.

### Aggiungere il peer sul server

Tornate sul server e aggiungete un blocco `[Peer]` per questo client (o create il file con tutti i peer fin da subito, se sapete già quanti client collegherete):

```ini
[Peer]
# laptop-01
PublicKey = <chiave pubblica del client>
AllowedIPs = 10.66.0.2/32
```

Salvate e riavviate il servizio del tunnel perché rilegga la configurazione:

```powershell
& "C:\Program Files\WireGuard\wireguard.exe" /uninstalltunnelservice wg0
& "C:\Program Files\WireGuard\wireguard.exe" /installtunnelservice C:\WireGuard\wg0.conf
```

## Verificare che tutto funzioni

Sul client, attivate il tunnel dall'app WireGuard e controllate nella finestra principale: dovreste vedere l'host del server, i contatori di traffico in salita/discesa che si muovono, e l'orario dell'**ultimo handshake** aggiornarsi periodicamente. Se l'handshake non compare mai, il problema è quasi sempre a livello di rete (porta non raggiungibile, firewall, port forward mancante) prima ancora che di configurazione WireGuard.

Poi, da riga di comando sul client:

```powershell
ping 10.66.0.1
```

Se risponde, il tunnel funziona. Per verificare l'accesso alla LAN dell'ufficio (se l'avete abilitato, vedi sotto), provate a raggiungere una risorsa nota, ad esempio `ping 192.168.1.10` o l'apertura di una condivisione file.

> **Nota:** se il ping verso `10.66.0.1` funziona ma quello verso la LAN (`192.168.1.x`) no, il tunnel va bene: manca solo l'**IP forwarding** sul server, descritto nella prossima sezione.

## Tunnel completo o split tunnel?

Il campo `AllowedIPs` nel blocco `[Peer]` del client decide cosa passa dentro la VPN:

- **Tunnel completo** — `AllowedIPs = 0.0.0.0/0, ::/0`: tutto il traffico del client, incluso quello verso Internet, passa dal server. Utile se non vi fidate della rete su cui siete (Wi-Fi pubblico) o se volete che il client "esca" sempre con l'IP del server.
- **Split tunnel** — `AllowedIPs = 10.66.0.0/24, 192.168.1.0/24`: solo il traffico verso la VPN e la LAN dell'ufficio passa dal tunnel, il resto (Netflix, siti web, tutto il resto) esce direttamente dalla connessione del client. Più leggero per il server, e per l'utente spesso più veloce.

In entrambi i casi, se volete che i client raggiungano host della **LAN reale** (non solo il server), Windows deve fare da router fra l'interfaccia WireGuard e quella di rete fisica. Per impostazione predefinita non lo fa: va abilitato l'**IP forwarding**:

```powershell
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name "IPEnableRouter" -Value 1
Restart-Computer
```

Se invece volete il **tunnel completo** (i client escono su Internet passando dal server), serve anche il **NAT** in uscita sull'interfaccia fisica del server:

```powershell
New-NetNat -Name WireGuardNAT -InternalIPInterfaceAddressPrefix 10.66.0.0/24
```

Questo comando basta da solo, senza installare il ruolo Routing and Remote Access: il modulo `NetNat` è incluso in Windows Server dal 2016 in poi.

## Qualche accorgimento di sicurezza

- **Una coppia di chiavi per dispositivo**, mai condivisa fra più persone: è l'unico modo per poter revocare l'accesso a *un* dispositivo (basta togliere il suo blocco `[Peer]` dal server) senza dover ruotare le chiavi di tutti gli altri.
- **`AllowedIPs` il più stretto possibile** per ogni peer sul server: un client che si occupa solo di backup non ha bisogno di poter raggiungere l'intera LAN.
- **Cambiare la porta di default** (51820) non è vera sicurezza — è *security through obscurity* — ma riduce parecchio il rumore di fondo degli scanner automatici che bussano sulla porta standard nei log.
- **WireGuard non sostituisce l'autenticazione applicativa**: dà accesso di rete, non identità utente. Se dietro la VPN c'è RDP, una share file o un pannello di amministrazione, tenete comunque password forti e, dove possibile, MFA su quei servizi — la VPN è un livello, non l'unico.
- **Backup delle chiavi private** in un posto cifrato (password manager, non un file di testo sul desktop): se perdete quella del server dovrete rigenerarla e riconfigurare ogni client.

## Perché è così veloce

Vale la pena spendere due righe sul "veloce" del titolo. Su Windows, dalla versione che usa il driver **WireGuardNT**, l'intero percorso dei pacchetti gira **nel kernel**, non più in un processo user-space come nelle prime versioni (che si appoggiavano a `wireguard-go` sopra l'adattatore Wintun). Questo, insieme al fatto che il protocollo non ha l'overhead di negoziazione di IPsec (niente IKE, niente rinegoziazioni continue) e non soffre del rallentamento tipico di OpenVPN in TCP, si traduce in throughput molto vicini al limite della connessione fisica e in una latenza aggiuntiva minima — nella pratica, spesso impercettibile rispetto al traffico non incapsulato.

## Conclusioni

Messo in piedi una volta, un tunnel WireGuard fra Windows Server e Windows 11 richiede pochissima manutenzione: nessun certificato da rinnovare, nessuna lista di cifrari da tenere aggiornata, un file di configurazione per peer. I punti dove ci si incastra di solito sono sempre gli stessi tre: **porta UDP non raggiungibile** (firewall o port forward mancante), **IP forwarding disattivato** (niente accesso alla LAN) e **NAT mancante** (niente Internet in tunnel completo) — se il tunnel si stabilisce (handshake visibile) ma qualcosa dopo non funziona, è quasi sempre uno di questi tre.

## Download

- [WireGuard per Windows](https://www.wireguard.com/install/) — stesso installer per server e client, sito ufficiale
- [wg0-server.conf](/static/assets/files/blog/wireguard-windows/wg0-server.conf) — template di configurazione per il server, con due peer di esempio
- [client.conf](/static/assets/files/blog/wireguard-windows/client.conf) — template di configurazione per il client, con entrambe le varianti (tunnel completo / split tunnel) commentate

## Riferimenti

- [wireguard.com](https://www.wireguard.com/) — sito ufficiale del protocollo
- [Documentazione WireGuard per Windows](https://www.wireguard.com/install/){:target="_blank"} — pagina di download e note sul client
- [New-NetNat (documentazione Microsoft)](https://learn.microsoft.com/en-us/powershell/module/netnat/new-netnat){:target="_blank"} — dettagli sul cmdlet usato per il NAT in tunnel completo
