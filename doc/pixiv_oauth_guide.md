# Pixiv OAuth Guide

## Introduction

This guide will help you get your refresh token for Pixiv API calls.

*You can `ignore` this guide if you do not wish to download from Pixiv (Pixiv Fanbox is not affected).*

## Prerequisites

- You must have a Pixiv account.
- You are running Cultured Downloader as you follow this guide.

## Step 1: Obtaining the OAuth Login URL

1. Go to the settings by clicking the profile icon in the top right corner and click on `Settings`.
2. Go to the `Advanced` tab and click on `Start OAuth` under `Pixiv Mobile OAuth Refresh Token`.
3. A new tab will open in your default browser and you will be prompted to log in to Pixiv.
4. ***Important: Do NOT sign in yet!***

<img src="/res/guide/pixiv_oauth/step-1.png" alt="step 1" style="width: 70%;">

## Step 2: Before signing in

1. Right click and click on `Inspect` to open the developer tools.
   - Alternatively, you can press `F12` to open the developer tools.
   - This assumes that you are using Google Chrome, for other browsers, it may be different.
2. Click on the `Network` tab and enable `Preserve log` by ticking it.

<img src="/res/guide/pixiv_oauth/step-2.1-2.2.jpg" alt="step 2.1 to 2.2" style="width: 70%;">

3. Now you can login but do not close your developer tools yet.

## Step 3: After signing in

1. You will notice that you will be redirected to an empty page. Do not worry, this is normal.
2. Scroll down to bottom in the `Network` tab under the developer tools and you will see a text highlighted in red.

<img src="/res/guide/pixiv_oauth/step-3.2.jpg" alt="step 3.2" style="width: 70%;">

3. Click on it and copy the code from the `Request Headers` tab.
   - The request URL should be something like this:
     -  `pixiv://account/login?code=<refresh_token>&via=login`
     - Example:
       - `pixiv://account/login?code=AX3456789wataMeef_-1234568FGGj_-B2A1RDYornt&via=login`
       - We will only need to copy code part, which is `AX3456789wataMeef_-1234568FGGj_-B2A1RDYornt`.

<img src="/res/guide/pixiv_oauth/step-3.3.jpg" alt="step 3.3" style="width: 70%;">

1. Using the example above, the code we got was `AX3456789wataMeef_-1234568FGGj_-B2A1RDYornt`. We can then use this code and paste it on Cultured Downloader and submit it.
2. You will be notified that the refresh token has been saved.
