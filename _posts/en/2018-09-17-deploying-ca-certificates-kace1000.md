---
title: How to import a CA certificate on Windows PCs with Kace 1000
layout: post
date: '2018-09-17 11:30:00'
description: Let's see together how to deploy Windows certificates using KACE 1000
lang: en_US
image: "/static/assets/img/blog/ssl.png"
categories:
- Kace
permalink: "/en/blog/kace/:title/"
translation_key: ca-certificate-deployment-kace1000
keywords: kace,k1000,script,batch,ssl,certificate,certutil,kscript
tags:
- kace
- k1000
- script
- batch
- kscript
- ssl
- ca root
- certificate
- security
icon: fa-floppy-o
intro: In a professional environment, where it's good practice for Windows users to
  have no local admin rights, even installing a simple CA can be a hassle, since it
  often requires the IT department in charge of user support to step in.
---

There are several methods for installing certificates transparently, the most obvious and common of which is undoubtedly a _GPO_. But a GPO isn't always the fastest solution (for example: whoever needs to deploy the certificates might not have permissions to work on GPOs, or the certificate might only need to be installed on a handful of PCs, so whoever should create the GPO doesn't treat it as a priority and the timeline risks stretching out)

So let's see how to **deploy a self-signed CA certificate via KACE 1000**. Afterwards, using the same procedure, we'll also install a second, intermediate certificate on the clients, itself validated by the CA.

* TOC
{:toc}

# The certutil.exe utility
certutil.exe is a utility, present on every Windows system, that lets us do a lot of things with certificates.
We can convert them if the format we have isn't the one we need, import and export them (both locally and to Active Directory), verify the validity of private/public key pairs, and so on.

It's used from the command line, and for the full syntax I'll point you to the [dedicated page](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/certutil){:target="_blank"} on the Microsoft Knowledge Base

## Definitions

- Both of our certificates are already in .cer format
- The CA certificate is called NGIRootCA01
- The intermediate certificate is called NGISSLCA01.cer

## Importing the CA via certutil.exe

The import command, which we can run from any administrative prompt, is the following

```batch
start /wait certutil -addstore Root NGIRootCA01.cer
```

The -addstore parameter defines the datastore where we'll install the certificate. *Root* corresponds to "**Trusted Root Certification Authorities**"


## Importing the intermediate certificate

The intermediate certificate (which we'll call SSLCA01.cer) referenced earlier is imported the same way, only changing the target datastore:

```msdos
start /wait certutil -addstore CA NGISSLCA01.cer
```


# The kscript on Kace

Now let's bring all of this over to Kace 1000, by creating a dedicated script.

## Task summary

- Setting up the basic parameters
- Importing the two certificates as dependencies
- Creating a batch file
- Scheduling

## Building it

1. Go to _Scripting / Scripts_ and create a new kscript ("_New_")  
2. Once you've given it a name, go to the _Operating Systems_ section and click **Manage Operating Systems**, selecting all the Windows OSs (and, since we're going to create a batch file, **only** the Windows ones) you're interested in  
  ![kscript Manage Operating Systems](/static/assets/img/blog/kace/cassl/oss.png)  
3. Verify that _Windows Run As_ is set to **Local System**  
  ![kscript Run As](/static/assets/img/blog/kace/cassl/runas.png)  
4. In the **Dependencies** section, click **+New Dependency...** and upload:

   1. The Root certificate
   2. The Intermediate certificate  
   ![kscript Certificates](/static/assets/img/blog/kace/cassl/certificati.png) 
5. Now click **+Task...** in the section below and set up the following steps:

   1. **Verify** that the file "C:\Tools\certificato.ok" exists (this will let us check whether the certificate has already been applied — since we'll schedule this script to run at regular intervals, if the _certificato.ok_ file exists the script stops right there). For reference on why this path was chosen, see [this earlier article of mine](/en/blog/kace/k1000-report-pc-with-smartcard-reader/){:target="_blank"}
   2. **On Success**: nothing
   3. **Remediation**: Run the batch file "_Install_CA_Root_Script_" with params ""  
    ![kscript Script](/static/assets/img/blog/kace/cassl/script.png)  
    Code:
    ```dosbatch
    @echo off
    start /wait certutil -addstore Root NGIRootCA01.cer
    start /wait certutil -addstore CA NGISSLCA01.cer
    exit
    ```  
   4. **On Remediation Success** Launch a program...  
    ![kscript Remediation](/static/assets/img/blog/kace/cassl/remediation.png)  

6. Click **Save** to finish creating the kscript

## Scheduling

If we want to schedule the script, once back in editing mode it's enough to set the desired window.
For example, in our case the script will run on the target devices every three hours, following this logic:

   1. The script runs for the first time
   2. When it finishes, it leaves a "_certificato.ok_" file, 0 bytes in size, in C:\Tools\
   3. From the next run onward (every three hours...) if it finds the "certificato.ok" file, it stops and does nothing else

![kscript Schedule](/static/assets/img/blog/kace/cassl/schedule.png)  
