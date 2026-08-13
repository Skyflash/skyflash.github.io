---
layout: post
title:  "Application Control with K1000"
date:   2018-07-11
description: "How to use KACE 1000 to control and block unauthorized software on PCs - A short guide."
intro: "Once the blocklist has been set up, when a user tries to open an unauthorized piece of software they'll get a warning in the bottom-right corner of the screen instead."
lang: en_US
image: /static/assets/img/blog/kace/smartcard/kace.jpg
keywords: "kace,k1000,script,vbs,visualbasic,smartcard,security,encryption"
categories: [Kace]
permalink: "/en/blog/kace/:title/"
translation_key: application-control-k1000
tags: [kace,script,vbs,smartcard,security,encryption]
icon: fa-unlock
---

This quick guide assumes the reader already has a good understanding of the KACE 1000 (KACE SMA) environment and of how Labels work

* TOC 
{:toc}

# Application control with K1000, step by step

Application control on Kace works with a two-part logic:

1. A [_Label_](#the-label), able to control and block software

2. One or more Software titles marked as [_Not Allowed_](#the-software-to-block)

For it to work, **both** conditions must be **true**

## The Label

Kace ships with a Label already pre-configured, using default parameters.

We'll use this one to walk through how application control works.

![Screenshot 1 - Default Application Control Label]({{ site.img_path }}/kace/appcontrol/K1000_appcontrol.png)

1. Go to _Home_, then to _Label Management_, and select **Labels**

2. Our default label is called **"ApplicationControlDevices"** and is configured like this:  

![Screenshot 2 - Appcontrol Label Details]({{ site.img_path }}/kace/appcontrol/appcontrol_label.png)

### What the Label means

Let's quickly go over what each flag means:

* Device Inventory: The Label applies to the device Inventory (i.e. PCs)
    * Allow Application Control: The Label is able to control the launching of applications
* Resources (Processes, Services, Startup Items): The Label can also be applied to processes and services
* Catalog: The Label applies to the Software Catalog (**essential** for the blocking mechanism to work properly!)
* Software: Same as above, but for software not normalized by the catalog

## The software to block

Let's head to the **Software Catalog** (*Inventory* -> *Software Catalog*), which groups and "normalizes" all detected and recognized software under a single name. To be clearer, we'll have for example "iTunes 12.x", which covers every revision of iTunes 12 (e.g. 12.1, 12.4, 12.74, and so on).

_Working from the Software Catalog lets us block or monitor a piece of software regardless of the updates it receives._

![Screenshot 3]({{ site.img_path }}/kace/appcontrol/appcontrol_software_catalog.png)

Once we've found our software (let's keep using iTunes 12.x as an example), select the checkbox and from the "Choose Action" menu pick "**Mark Not Allowed**"  
  
Alternatively, you can check "**Not Allowed**" directly on the software's own detail page. Autosave kicks in as soon as you change the checkbox selection.  
  
![Screenshot 4]({{ site.img_path }}/kace/appcontrol/software_catalog_detail.png)

## The PCs and their Label

Now that we understand how both the Label (which applies to PCs) and the block marker (which applies to software) work, we can put them together to get the effect we want.

**NOTE:** *Kace's mechanism will only block programs from opening on PCs that have the "ApplicationControlDevice" Label applied — and only on those*. During this experimental phase, the label is NOT applied by default to every inventoried device, so this has to be done manually.

**A PC that has a blocked piece of software but doesn't belong to the Label will keep running that software as if nothing happened, with no issues at all.**

* 1 Get the name(s) of the PC(s) you want to add to the Label. There are several ways to do this, all equally valid:  
    1. You already know it and can find it directly in Inventory
    2. From the Software Catalog, click the number in the "Installed" column, which will take you to the list of all PCs with that software  

![Screenshot 5]({{ site.img_path }}/kace/appcontrol/appcontrol_locked.png)

* 2 Check the checkbox next to the PC(s) you're interested in and from the "**Choose Action**" menu click "**Apply Labels**"  

![Screenshot 6]({{ site.img_path }}/kace/appcontrol/apply_label.png)

* 3 Choose the "**ApplicationControlDevices**" Label and drag it into the right-hand side of the window, then click "**Apply Labels**"

![Screenshot 7]({{ site.img_path }}/kace/appcontrol/labels_list.png)

## Inventory

We've made the rules. We've applied the Labels. Is anything still missing?

One of the strengths of the Kace agent is that it works essentially offline: it connects to the server once, receives all the rules, information, and scripts, and then keeps working on its own, without needing to talk to the server again. And it keeps doing everything it's been told to do until told otherwise. This mechanism is called "Inventory", and in our case it runs once every 8 hours (at minimum) on every single inventoried computer.

*New blocking rules, then, will be applied to the PC the next time it checks in (i.e. at its next inventory)*. We can force this manually (click the device's box, then "**Force Inventory**"), but under normal conditions the results of our rules will only show up after a few hours (and a PC restart), not in real time.

# The end result

![Screenshot 8]({{ site.img_path }}/kace/appcontrol/final_result.png)

Once the blocklist has been created (some software titles in this image are purely for illustration purposes and aren't actually meant to be blocked), the Label assigned to the PC, and the rules propagated through inventory, once the user tries to open the software they'll get an alert in the bottom-right corner of the screen, like this one:

![Screenshot 9]({{ site.img_path }}/kace/appcontrol/messagebox.png)
