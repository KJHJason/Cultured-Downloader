# Session Cookie Guide

## Introduction

This guide will help you get your session cookie needed for Cultured Downloader to download from the various platforms.

## Using Get cookies.txt LOCALLY

This is by far the most user-friendly method to obtain the session cookie if you're not familiar with your browser's developer tools.

### Step 1: Obtaining the cookies text/json file

1. Go to [Get-cookies.TXT-Locally Repository](https://github.com/kairi003/Get-cookies.txt-LOCALLY?tab=readme-ov-file#installation) and click on the provided link according to your browser to download the browser extension.
2. Go to the respective platform's website and log in if you have not done so.
3. Click on the extension icon and click on `Get cookies.txt`.
4. Finally, you can now export it as a `txt` or `json` file based on the export format selected.

<img src="/res/guide/session_cookie/step-1.png" alt="step 1" style="width: 70%;">

### Step 2: Upload the exported file

1. After obtaining the `txt` or `json` file, click on the `Upload` button on Cultured Downloader and you're done!.
   - Note: Even though I said "upload", this doesn't mean that the file is being uploaded to somewhere. It is just being uploaded to the Go/Golang backend for processing and verification. 

<img src="/res/guide/session_cookie/step-2.png" alt="step 2" style="width: 70%">

## Using Browser's Developer Tools

This method is more technical and you might get lost if you're unfamiliar with your browser's developer tools.

### Step 1: Opening the developer tools

1. Right click and click on `Inspect` to open the developer tools.
   - Alternatively, you can press `F12` to open the developer tools.
   - This assumes that you are using Google Chrome, Mozilla Firefox, or Microsoft Edge. For other browsers, it may be different.
2. For Google Chrome and Microsoft Edge, click on the `Application` tab. For Mozilla Firefox, click on the `Storage` tab.

Google Chrome:

<img src="/res/guide/session_cookie/chrome.png" alt="chrome application tab" style="width: 70%">

Microsoft Edge:

<img src="/res/guide/session_cookie/edge.png" alt="edge application tab" style="width: 70%">

Mozilla Firefox:

<img src="/res/guide/session_cookie/firefox.png" alt="firefox storage tab" style="width: 70%">

### Step 2: Finding the session cookie and copying it

1. Look for the `Cookies` section and click on the respective platform's website.
2. After that look for the corresponding session cookie name and copy the value.
   - For example, for Fantia, the session cookie is `_session_id`.
   - If you are unsure about the cookie name, it is listed in brackets in Cultured Downloader under the `Sessions` settings tab.

### Step 3: Saving the session cookie

1. Paste the copied session cookie into the respective platform's session cookie field in Cultured Downloader.
2. Click on the `Save` button and you're done!
