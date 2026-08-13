---
title: Deploying a Windows 10 feature update via Kace
layout: post
date: '2019-12-16 11:30:00'
description: Using Kace to upgrade a PC from Windows 7/8/10 to the latest Windows 10 build
lang: en_US
image: "/static/assets/img/blog/kace/smartcard/kace.jpg"
categories:
- Kace
permalink: "/en/blog/kace/:title/"
translation_key: windows10-build-upgrade-kace
keywords: kace,k1000,script,batch,windows,windows10,upgrade,kscript
tags:
- kace
- k1000
- script
- batch
- kscript
- windows
- windows 10
- upgrade
icon: fa-floppy-o
intro: Windows 10 feature updates, like the "Fall Creators Update" or the "April 2018 Update", aren't available through KACE's patch feed. As an alternative, these updates can still be deployed using a Managed Install.
---

Windows 10 feature updates aren't traditional *patches*, *rollups* or *service packs*. From a deployment standpoint, they're designed and behave like an *"in-place"* OS upgrade — meaning they don't touch any existing data or settings, remove the previous OS version, or save any data. Because of this, they require more planning and testing than traditional patches, along with more resources (disk space on both server and clients, bandwidth, installation time, and so on).

<small><b>NOTE: this guide uses the October 2019 1903 build as an example throughout the following steps</b></small>

* TOC
{:toc}

## First step: Create the installation package

Feature updates must be obtained directly from Microsoft. They're distributed as an ISO and need to be extracted and repackaged for deployment through third-party products like the KACE Systems Management Appliance.

### Get an official Windows 10 ISO

To get the Windows 10 ISO we'll use **any one** of these **three methods**:

1. Download the ISO from your own **MSDN Library** (requires an active MSDN license), making sure to grab the edition appropriate for your purpose (e.g. Home, Professional, etc.)
2. Use Microsoft's **Media Creation Tool**, downloadable from this address: [https://www.microsoft.com/en-us/software-download/windows10](https://www.microsoft.com/en-us/software-download/windows10)
     1. Once downloaded, run the Tool
     2. When asked what you want to do, choose "**Create installation media (USB flash drive, DVD, or ISO file) for another PC**" and click **Next**
     3. Verify that the recommended options (language, edition, and architecture) match your needs and proceed
     4. On "Choose which media to use", select **ISO file** and click **Next**
     5. Choose a name for the file (example: **Windows10_1903_English_x64.iso**) and continue. The download will start for the ISO configured with the options you chose above
     6. Click **Finish** once it completes to close the wizard
3. *Alternative method: download the ISO directly from [https://www.microsoft.com/en-us/software-download/windows10ISO](https://www.microsoft.com/en-us/software-download/windows10ISO), visiting the URL from a **non-Windows** computer (macOS or Linux)*

### Mount the ISO and create a .zip file

1. On Windows 10, the ISO can be mounted by right-clicking the file and choosing "**Mount**", or simply double-clicking the ISO file.
2. Make sure 7-Zip is installed. 7-Zip is a hard requirement, so if you don't have it, grab it from [here](https://www.7-zip.org/a/7z1604.exe)
3. Once mounted, **select all the files inside the ISO** (not the directory/drive itself, but the files inside it), then right-click and choose "**7-Zip > Add to archive...**"
![Screenshot 1 - 7-Zip > Add to Archive...]({{ site.img_path }}/kace/w10upgrade/KB_1-547AMZ0_AddToArchive.png)
4. **Note:** since the ISO is obviously read-only, choose an external save path for the zip, somewhere on your hard disk
5. Once compression finishes, the zip file will be created at the chosen location with an auto-generated name (example: setup.zip). Rename it appropriately (example: **Windows10_1903_English_x64.zip**). This file will be used in the following steps
6. Unmount the ISO (right-click the drive and eject) and do whatever you like with it — we won't need it again for this guide

## Second step: Upload the package to KACE SMA

Because of the limit on the maximum uploadable file size through the web interface, the zip package needs to be uploaded to Kace via the **clientdrop Samba share**. The maximum file size for upload through the SMA Web UI is in fact 2GB (version 8.0 and earlier) or 4GB (version 8.1 and later), while feature update packages tend to run slightly over these limits. The Samba method sidesteps the upload limit entirely and, in my opinion, is also faster and more convenient.

### Check that Samba is enabled

1. If Samba isn't enabled, enable it (Samba can be disabled again once the package has been uploaded and imported in step 3). The Samba enable/disable settings live under **Settings > Security Settings** in the Admin interface. To enable Samba, make sure the "**Enable organization file shares**" checkbox is checked
![Screenshot 2 - Samba Shares]({{ site.img_path }}/kace/w10upgrade/KB_1-547AMZ0_w10bu_samba.png)
2. Also make sure the share is enabled at the **organization level** too, and that you know the credentials for the **clientdrop** share. If not, the password can be reset from the **Settings > General Settings** page in the Admin UI (organization-specific on multi-org systems)
![Screenshot 3 - Samba Shares]({{ site.img_path }}/kace/w10upgrade/KB_1-547AMZ0_w10bu_samba_share.png)

### Upload the archive to clientdrop

1. Connect to the **clientdrop** share. You can do this easily by opening File Explorer and typing the UNC address of your Kace appliance (example: __\\\KBOX\clientdrop__, replacing _KBOX_ with your SMA host's name).
![Screenshot 4 - KACE SMA clientdrop]({{ site.img_path }}/kace/w10upgrade/KB_1-547AMZ0_w10bu_clientdrop.png)
2. Drag the .zip file created in [Step One](#first-step-create-the-installation-package) into the **clientdrop** share
3. ![Screenshot 5 - KACE SMA clientdrop]({{ site.img_path }}/kace/w10upgrade/KB_1-547AMZ0_w10bu_clientdrop_copy.png)
4. Once the upload completes successfully, move on to Step 3

## Third step: Map the installation package inside Inventory

### Operational scenario

For performance reasons, we'll create a **Custom Software Title** inside the **Software Inventory**, rather than using the **Software Catalog**. This choice is due to the sheer number of Windows 10 versions and revisions in the Catalog, which would heavily impact Kace's database performance on every query issued by the Managed Install we'll set up toward the end of this guide.

We'll also create a dedicated **Custom Inventory Rule**, to have more precise and granular control over the current and future upgrade process.

### Create a Custom Software title

1. In the Admin interface, go to **Inventory > Software**
2. From the **Choose Action** menu, select **New**
3. Fill in the **Name**, **Version**, **Publisher** and **Notes** fields as you prefer. For example:
![Screenshot 6 - Custom Inventory Title]({{ site.img_path }}/kace/w10upgrade/customsoftware.png)
4. In the **Custom Inventory Rule** field, enter a rule that checks a specific registry key, located at **HKLM\Software\Microsoft\Windows NT\CurrentVersion**, to identify the build version.
![Screenshot 7 - Custom Inventory Rule]({{ site.img_path }}/kace/w10upgrade/cir1903.png)  
Code:
```dosbatch
RegistryValueEquals(HKLM64\SOFTWARE\Microsoft\Windows NT\CurrentVersion,ReleaseId,1903)
```
5. Finally, associate our zip file — created earlier and copied to the clientdrop share — with the Custom Software. To do this, choose the file from the **Upload and Associate Client Drop File** dropdown, then save.
![Screenshot 8 - Media Upload]({{ site.img_path }}/kace/w10upgrade/mediaupload.png)

## Fourth step: Create and deploy the upgrade process

Now that we have all the pieces of the puzzle, we just need to put them together in this final step. We'll create a **Managed Install** whose job will be to deploy the new Windows 10 build to the target PCs.<br>
We'll go through each step one by one, but if you're already familiar with Managed Installs, feel free to skip straight to the end.

### Create the Managed Install

1. In the Admin panel, go to **Distribution > Managed Installations**
2. Select **Choose Action > New**
3. Type a name for the Managed Install, for example "Windows 10 1903 Upgrade"
4. Set the desired run option based on your requirements. If you leave the field set to "Disabled" the MI won't run
5. Under **Inventory**, choose **Software**
6. In the **Software** dropdown, choose the software title you created in [Step 3](#third-step-map-the-installation-package-inside-inventory) and associated the zip with
7. Verify that **Use associated file** is selected and that the file shown is your zip
![Screenshot 9 - Managed Install - General Settings]({{ site.img_path }}/kace/w10upgrade/mi-general.png)
8. If you'd like (recommended), select **Delete downloaded files**
9. **Installation Options:**
   1.  Select **Override default installation** and enter this string  
  Code:
  ```dosbatch
  setup.exe /auto upgrade /DynamicUpdate disable /showoobe none
  ```
   2.  Verify that the **Don't prepend msiexec.exe** checkbox is checked  
![Screenshot 10 - Managed Install - Options]({{ site.img_path }}/kace/w10upgrade/mi-options.png)
    * **Note**: You can find an exhaustive explanation of all **setup.exe** parameters on Microsoft's technet, here: [https://blogs.technet.microsoft.com/home_is_where_i_lay_my_head/2015/09/14/windows-10-setup-command-line-switches/](https://blogs.technet.microsoft.com/home_is_where_i_lay_my_head/2015/09/14/windows-10-setup-command-line-switches/)

### Deploy

1. In the **Deploy** section, assign the **Labels** you find most appropriate to the Managed Install (*running one or more preliminary tests on a small number of computers is **strongly recommended***)
2. Configure the **Notification** section, entering a clear message that fits your needs
![Screenshot 11 - Managed Install - Schedule]({{ site.img_path }}/kace/w10upgrade/mi-schedule.png)
3. Configure the **Schedule**, again based on your specific needs (*Note: adjusting the deployment window isn't recommended, since MIs only run during the inventory interval. If the window is configured so that it isn't open long enough for all systems to complete an inventory cycle, affected systems will never receive the update.*)
![Screenshot 12 - Managed Install - Schedule]({{ site.img_path }}/kace/w10upgrade/mi-deployment.png)
4. Click **Save** to finish the job. That's it, happy build upgrading!

(remember: **ALWAYS TEST BEFORE DEPLOYING!!!**)
