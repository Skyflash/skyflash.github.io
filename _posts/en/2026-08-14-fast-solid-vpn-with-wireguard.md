---
title: "A fast, solid VPN with WireGuard: from Windows Server 2022 to Windows 11"
layout: post
date: '2026-08-14 00:15:00'
description: "A practical guide to a WireGuard VPN with server on Windows Server 2022 and clients on Windows 11: keys, config, port forwarding, full vs split tunnel, and security tips."
intro: "WireGuard doesn't need much of an introduction: tiny codebase, modern cryptography, and throughput that OpenVPN and IPsec can only dream of. What's missing out there is a guide that starts from a concrete, common case — server on Windows Server 2022, client on Windows 11 — without glossing over the steps that aren't as obvious on Windows as they are on Linux."
image: "/static/assets/img/blog/wireguard-windows/cover.png"
image_dark: "/static/assets/img/blog/wireguard-windows/cover-dark.png"
lang: en_US
featured: true
categories:
- Infrastructure & Systems
keywords: wireguard, vpn, windows server 2022, windows 11, networking, security, tunnel, powershell, nat
tags:
- windows-server
- windows11
- vpn
- wireguard
- networking
- security
permalink: "/en/blog/infrastructure/:title/"
translation_key: wireguard-windows-server-2022-vpn
icon: fa-lock
---
I'm Fortinet NSE6 certified and know how to build VPNs, but when I need something ready to go in a few clicks — including onboard VPNs on Mikrotik routers, to reach a client's whole network — I reach for **WireGuard**: less configuration, fewer things that break, and speed OpenVPN and IPsec can't get close to. The protocol was born on Linux, but the official Windows client has been mature for a while, and since the **WireGuardNT** driver (kernel-level, no longer the old user-space `wireguard-go`) Windows performance is fully in line with Linux.

In this article we'll set up a very common scenario: a **WireGuard server on Windows Server 2022** acting as the entry point for one or more **Windows 11 clients**, with access to the office LAN and, optionally, a full tunnel that also routes Internet traffic. I'll use generic names and IP addresses — swap in your own before going to production.

* TOC
{:toc}

## Why WireGuard over OpenVPN or IPsec

A few numbers and concrete reasons, without dragging this out:

- **Tiny codebase**: WireGuard's core is a few thousand lines, versus OpenVPN's hundreds of thousands. Less code means a smaller attack surface and a much simpler security review.
- **Modern, non-negotiable cryptography**: Curve25519, ChaCha20-Poly1305, BLAKE2s. There's no cipher list to configure and no legacy algorithms to disable by hand — WireGuard uses one up-to-date suite, full stop.
- **UDP only**: no "TCP-over-TCP meltdown" (the slowdown typical of OpenVPN over TCP on lossy networks).
- **Instant roaming**: a client can switch networks — home Wi-Fi to mobile data, one hotel to another — without renegotiating the tunnel. The server notices the new source IP on the first valid packet and just continues.
- **No sessions, no server-side state** until traffic actually arrives: the server doesn't keep a process hanging around per connected client.

The flip side: WireGuard **has no concept of user/password**. A peer's identity is its public key, period. If you need per-user, "enterprise-style" authentication, you build it on top (one keypair per person/device, never shared) — more on that in the security section below.

## Prerequisites

- A **Windows Server 2022** with a public IP address, or behind a router where you can set up port forwarding.
- One or more **Windows 11** machines to connect over VPN.
- The official **WireGuard for Windows** client, same installer on server and clients (link in the [Download](#download) section).
- Administrative access on both machines, and the ability to open a UDP port on the firewall (and on the router, if the server sits behind NAT).
- If you want clients to reach the office LAN too (not just the server), a bit of address planning — see the diagram below.

## Architecture and addressing scheme

The reference scenario we'll use throughout the article:

![Diagram: a Windows 11 client, an encrypted WireGuard tunnel across the Internet and a router doing NAT/port-forward on UDP port 51820, to the Windows Server 2022 server, which also exposes the office LAN 192.168.1.0/24](/static/assets/img/blog/wireguard-windows/diagram-topology.png)

- WireGuard network: **10.66.0.0/24** (a subnet dedicated to the VPN, separate from the real LAN — this avoids routing conflicts).
- Server: VPN address `10.66.0.1`, LAN address `192.168.1.10`.
- Clients: `10.66.0.2`, `10.66.0.3`, etc. — one address per device.
- Listening port: **UDP 51820** (the default; you can change it, see the security section).
- Office LAN to reach over VPN: `192.168.1.0/24`.

> **Note:** if the server sits behind a router (e.g. a home connection, or an office without a direct public IP), you need a **UDP 51820 port forward → the server's LAN address**. If the public IP isn't static, add a DDNS (Dynamic DNS) service and use the hostname instead of the IP in the client's `Endpoint`.

## Setting up Windows Server 2022

Install [WireGuard for Windows](https://www.wireguard.com/install/){:target="_blank"} using the official MSI (the same installer as the client). The app opens with a tunnel management panel: we'll only use it to generate keys the first time, because on a server the right approach is to run it **as a Windows service**, not leave it tied to a logged-in session.

### Generating the server's keypair

From the app's **Manage tunnels** panel, choose **Add Tunnel > Add empty tunnel...**: a fresh keypair is generated right away, with the private key already filled into the config editor and the matching public key shown in the tunnel's detail panel. Copy the public key somewhere safe: you'll need it in every client's configuration.

> **Warning:** the private key is the only thing that identifies the server (or a client) on the VPN — treat it like a password. Don't send it over email or chat, don't put it in a repository, and if you suspect it's been exposed, regenerate it and update every peer.

### The server's config file

Replace the editor's content with something like this (adjusting addresses and keys):

```ini
[Interface]
PrivateKey = <server private key>
Address = 10.66.0.1/24
ListenPort = 51820

[Peer]
# laptop-01
PublicKey = <client public key>
AllowedIPs = 10.66.0.2/32
```

Each client gets its own `[Peer]` block, with its own public key and a single `/32` address (its own, not the whole subnet — that's how WireGuard knows which peer to route packets for that IP to). Save the file as `C:\WireGuard\wg0.conf`.

### Running the tunnel as a Windows service

On a server, avoid the GUI app's "Activate" button: that tunnel stays tied to the session of whoever started it and stops at logoff. The correct way is to install it as a **service**, so it starts on its own at boot and doesn't depend on any session:

```powershell
& "C:\Program Files\WireGuard\wireguard.exe" /installtunnelservice C:\WireGuard\wg0.conf
```

To stop or remove it later:

```powershell
& "C:\Program Files\WireGuard\wireguard.exe" /uninstalltunnelservice wg0
```

Check the service is running with `Get-Service WireGuardTunnel*`.

### Opening the port on the firewall and the router

On the Windows firewall:

```powershell
New-NetFirewallRule -DisplayName "WireGuard VPN" -Direction Inbound -Protocol UDP -LocalPort 51820 -Action Allow
```

If the server is behind a router, also add the UDP 51820 port forward there, pointing to the server's LAN address (`192.168.1.10` in our diagram).

## Setting up the Windows 11 client

### Generating the client's keypair

Same process as the server: install [WireGuard for Windows](https://www.wireguard.com/install/){:target="_blank"}, **Add Tunnel > Add empty tunnel...**, copy the generated public key (you'll need it for the `[Peer]` block on the server).

### The client's config file

```ini
[Interface]
PrivateKey = <client private key>
Address = 10.66.0.2/24
DNS = 192.168.1.1

[Peer]
PublicKey = <server public key>
Endpoint = vpn.yourdomain.com:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

A couple of fields worth explaining:

- **`Endpoint`**: the public address (or DDNS hostname) and port the client connects to. It's the only place that needs an "externally reachable" address — the server doesn't need to know the client's IP in advance.
- **`PersistentKeepalive = 25`**: sends an empty packet every 25 seconds to keep the client's router NAT mapping open. Without it, if the client sits behind NAT (almost always true on home or mobile networks), the tunnel can "fall asleep" and the server can no longer reach it first.
- **`AllowedIPs`**: this is where you decide between a full tunnel and a split tunnel — covered in the next section.

Import the file via **WireGuard > Import tunnel(s) from file...**, or paste the content directly into the empty tunnel's editor created earlier.

### Adding the peer on the server

Back on the server, add a `[Peer]` block for this client (or create the file with all peers from the start, if you already know how many clients you'll connect):

```ini
[Peer]
# laptop-01
PublicKey = <client public key>
AllowedIPs = 10.66.0.2/32
```

Save and restart the tunnel service so it picks up the new config:

```powershell
& "C:\Program Files\WireGuard\wireguard.exe" /uninstalltunnelservice wg0
& "C:\Program Files\WireGuard\wireguard.exe" /installtunnelservice C:\WireGuard\wg0.conf
```

## Checking that everything works

On the client, activate the tunnel from the WireGuard app and check the main window: you should see the server's host, the up/down traffic counters moving, and the **latest handshake** timestamp updating periodically. If the handshake never shows up, the problem is almost always at the network level (unreachable port, firewall, missing port forward) rather than in the WireGuard config itself.

Then, from the client's command line:

```powershell
ping 10.66.0.1
```

If it replies, the tunnel works. To check access to the office LAN (if you've enabled it, see below), try reaching a known resource, e.g. `ping 192.168.1.10` or opening a file share.

> **Note:** if pinging `10.66.0.1` works but pinging the LAN (`192.168.1.x`) doesn't, the tunnel itself is fine: you're just missing **IP forwarding** on the server, covered in the next section.

## Full tunnel or split tunnel?

The `AllowedIPs` field in the client's `[Peer]` block decides what goes through the VPN:

- **Full tunnel** — `AllowedIPs = 0.0.0.0/0, ::/0`: all of the client's traffic, including Internet traffic, goes through the server. Useful if you don't trust the network you're on (public Wi-Fi) or if you want the client to always exit with the server's IP.
- **Split tunnel** — `AllowedIPs = 10.66.0.0/24, 192.168.1.0/24`: only traffic to the VPN and the office LAN goes through the tunnel, everything else (Netflix, websites, everything else) goes straight out from the client's own connection. Lighter on the server, and often faster for the user.

Either way, if you want clients to reach hosts on the **real LAN** (not just the server), Windows needs to route between the WireGuard interface and the physical network interface. By default it doesn't: you need to enable **IP forwarding**:

```powershell
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name "IPEnableRouter" -Value 1
Restart-Computer
```

If you want a **full tunnel** instead (clients go out to the Internet through the server), you also need outbound **NAT** on the server's physical interface:

```powershell
New-NetNat -Name WireGuardNAT -InternalIPInterfaceAddressPrefix 10.66.0.0/24
```

That command is enough on its own, no need to install the Routing and Remote Access role: the `NetNat` module has shipped with Windows Server since 2016.

## A few security notes

- **One keypair per device**, never shared between people: it's the only way to revoke access for *one* device (just remove its `[Peer]` block on the server) without rotating everyone else's keys.
- **Keep `AllowedIPs` as narrow as possible** for every peer on the server: a client that only handles backups doesn't need access to the whole LAN.
- **Changing the default port** (51820) isn't real security — it's *security through obscurity* — but it noticeably cuts down the background noise of automated scanners knocking on the standard port in your logs.
- **WireGuard doesn't replace application-level authentication**: it grants network access, not user identity. If RDP, a file share or an admin panel sits behind the VPN, keep strong passwords and, where possible, MFA on those services too — the VPN is one layer, not the only one.
- **Back up private keys** somewhere encrypted (a password manager, not a text file on the desktop): lose the server's and you'll have to regenerate it and reconfigure every client.

## Why it's this fast

Worth spending a couple of lines on the "fast" in the title. On Windows, since the **WireGuardNT** driver, the entire packet path runs **in the kernel**, no longer in a user-space process like the early versions (which relied on `wireguard-go` on top of the Wintun adapter). That, combined with the protocol having none of IPsec's negotiation overhead (no IKE, no constant renegotiation) and none of OpenVPN's typical TCP slowdown, translates into throughput very close to the physical connection's limit and minimal added latency — in practice, often imperceptible compared to unencapsulated traffic.

## Wrapping up

Once set up, a WireGuard tunnel between Windows Server and Windows 11 needs very little maintenance: no certificates to renew, no cipher list to keep up to date, one config file per peer. The places people usually get stuck are always the same three: an **unreachable UDP port** (firewall or missing port forward), **IP forwarding disabled** (no LAN access), and **missing NAT** (no Internet in full-tunnel mode) — if the tunnel comes up (handshake visible) but something downstream doesn't work, it's almost always one of these three.

## Download

- [WireGuard for Windows](https://www.wireguard.com/install/) — same installer for server and client, official site
- [wg0-server.conf](/static/assets/files/blog/wireguard-windows/wg0-server.conf) — server config template, with two example peers
- [client.conf](/static/assets/files/blog/wireguard-windows/client.conf) — client config template, with both variants (full tunnel / split tunnel) commented

## References

- [wireguard.com](https://www.wireguard.com/) — the protocol's official site
- [WireGuard for Windows documentation](https://www.wireguard.com/install/){:target="_blank"} — download page and client notes
- [New-NetNat (Microsoft docs)](https://learn.microsoft.com/en-us/powershell/module/netnat/new-netnat){:target="_blank"} — details on the cmdlet used for full-tunnel NAT
