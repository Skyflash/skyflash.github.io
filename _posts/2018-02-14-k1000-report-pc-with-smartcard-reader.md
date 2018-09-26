---
layout: post
title:  "[K1000 Scripting] Find and report all PCs with a smartcard reader installed"
date:   2018-02-14
description: "Find and report all managed Windows PCs in K1000 Inventory with a smartcard reader installed."
intro: "The Custom Inventory Rule creates a new entry in every managed device. If a smart card reader has been discovered we’ll have at least one “DeviceClass: SMARTCARDREADER” text iside the Custom Inventory Fields section into every device record in Inventory / Devices"
lang: en_US
image: /static/assets/img/blog/kace/smartcard/kace.jpg
keywords: "kace,k1000,script,vbs,visualbasic,smartcard,security,encryption"
categories: [Kace]
tags: [kace,script,vbs,smartcard,security,encryption]
icon: fa-server
permalink: /blog/kace/:title/
---

# Target

Find and report all managed Windows PCs in K1000 Inventory with a smartcard reader installed.

## Overview

The script does not depend on K1000, so if you don't have KACE SMA in your environment don't worry: the script is still useful!

## Components

* [The Query] This script
* [The Automation] Kace Systems Management Appliance (AKA 'K1000')

## How it works

1. The vbs script executes a WMI query over the target device(s) and saves an output file named _smartcard.txt_ (see below in the [Setup section](#setup))
2. The vbs script is scheduled and deployed to the target device(s) via K1000 [_Online KScript_](#the-kscript)
3. A K1000 [_Custom Inventory Rule_](#the-custom-inventory-rule) reads the output file for every inventoried device and stores the information in the database
4. A scheduled [Report](#the-report) (choose your favorite format between HTML, CSV, PDF or Excel) returns only PCs with a smart card reader installed
5. Done!

## Setup

### The KScript (smarcard.vbs)

* Download [the script](/static/assets/files/blog/kace-smartcard/smartcard.vbs) or copy & paste the following code:

```bash
strComputer = "."
Dim log
Set log = Wscript.CreateObject("Scripting.Filesystemobject")
Set f = log.CreateTextFile("C:\Tools\smartcard.txt", 2)
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_PnPSignedDriver Where DeviceClass = 'SMARTCARDREADER'",,48) 
For Each objItem in colItems 
    f.WriteLine "DeviceClass: " & objItem.DeviceClass
Next
f.Close
```

* Edit **line 4** with the path where you want to save the output file. In our environment every PC has a _“C:\Tools”_ directory for service purpose, so I decided to save the output there.

```
Set f = log.CreateTextFile("C:\Tools\smartcard.txt", 2)
```

* Go to your _K1000 Dashboard_, then go to _Scripting_ and create a **New Script** (_Choose Action / New_)

* Name the script as your wish (for example: Check Smart Card Reader) and follow these steps:

#### Script Basic Settings

* Type: **Online KScript**
* Enabled: **Yes**
* Deploy: one or some devices, all devices or to a Device Label, according to your needs in your environment
* Windows Run As: **Local System**
* Upload the smartcard.vbs as **New Dependecy**

#### Tasks

We want the script to run once in every PC, so we'll use a “checkmark” (the smartcard.txt) to verify that...

* Verify: **Verify a file exists...**
    * C:\Tools\smartcard.txt
* Remediation: **Launch a program...**
    * Directory: **$(KACE_SYS_DIR)**
    * File: **cscript.exe $(KACE_DEPENDENCY_DIR)\smartcard.vbs**
    * Wait for completion: **Yes**
* On Remediation Success: **Upload a file...** (note: this step is not necessary and only for archiving purpose)
    * Directory: **C:\Tools**
    * File: **smartcard.txt**

...and **Save** your brand new script.

The Task and its steps are summarized in the following image. When you're ready, let's jump to the [Step 4!](#the-custom-inventory-rule)

![Screenshot 1]({{ site.img_path }}/kace/smartcard/screenshot1.png)

### The Custom Inventory Rule

1. In the K100 Dashboard, now go to _Inventory_ section, then go to _Software_ and create a **new Software entry** (_Choose Action / New_)

2. Name the rule as your wish (for example: IT Dep — Check Smart Card Reader) and follow these steps:

* Publisher: **IT Department** (it's useful for further searches into the _Software Inventory_)
* Supported Operating Systems: **All the Windows OSs in your Inventory**
* Custom Inventory Rule: `ShellCommandTextReturn(cmd /c type C:\Tools\smartcard.txt)`

...and **Save** your new Custom Inventory Rule.

Here's the summary image

![Screenshot 1]({{ site.img_path }}/kace/smartcard/screenshot2.png)

Now we need all our devices complete their inventory. The new Custom Inventory Rule creates a new entry in every device record managed by the K1000.

If a smart card reader has been discovered we'll have at least one “DeviceClass: SMARTCARDREADER” text iside the **Custom Inventory Fields** section into every device record in _Inventory / Devices_

![Screenhot 3]({{ site.img_path }}/kace/smartcard/screenshot3.png)

Otherwise, if a smart card reader has not been discovered, we'll have no text

When all your devices has been inventoried and you're ready, jump to the [next section](#the-report)

### The Report

In the K100 Dashboard, now go to _Reporting_ section, then in _Reports_ and create a new Report (_Choose Action / New_)

Name the Report as your wish (for example: PCs with Smart Card Reader) and follow these steps:

#### Title and Topic

* Category: **Inventory**
* Topic: **Device**

#### Fields to Display

* Device: **System Name**
* Operating System Info: **Name**
* User Information: **User Name**
* Manufacturer and BIOS: **System Model**

Feel free to add and modify any other field, according to your needings.

#### Filters

Delete the default filter and create this:

![Filter]({{ site.img_path }}/kace/smartcard/report1.png)

**Save** your new report and try it.
