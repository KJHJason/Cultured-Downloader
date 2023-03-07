# Google Drive API Key Guide

## Introduction

This guide will help you get your Google Drive API key required for downloading files from Google Drive.

*You can `ignore` this guide if you do not wish to download any Google Drive links from Pixiv Fanbox posts.*

## Step 1: Create a Google Cloud Platform Project and enable the Google Drive API

1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/).

<img src="/res/guide/gdrive_api_key/step-1.1.jpg" alt="step 1.1" style="width: 70%;">

2. Create a new project.
3. Give the project a name (any will do) and click `Create`.

<img src="/res/guide/gdrive_api_key/step-1.2-1.3.gif" alt="step 1.2 to 1.3" style="width: 70%;">

4. `IMPORTANT`: Please make sure to enable [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com) for the project. Otherwise, you will get a 403 Forbidden error when calling the Google Drive API.

<img src="/res/guide/gdrive_api_key/step-1.4.jpg" alt="step 1.4" style="width: 70%;">

## Step 2: Creating an API Key for GDrive API v3

1. Go to the `Credentials` page of your project under the `APIs & Services` tab.

<img src="/res/guide/gdrive_api_key/step-2.1.jpg" alt="step 2.1" style="width: 70%;">

2. Click on `CREATE CREDENTIALS` and select `API key`.

<img src="/res/guide/gdrive_api_key/step-2.2.jpg" alt="step 2.2" style="width: 70%;">

3. A prompt will appear with your API key. Copy the key as we will have to paste it when running the Cultured Downloader program.
   1. Please do ***NOT*** share your API key with anyone.
      - Note that you have a limit of 20,000 requests per every 100 seconds or 1 billion requests per day.
        - Usage limits reference: [https://developers.google.com/drive/api/guides/limits](https://developers.google.com/drive/api/guides/limits)
      - Hence, if it is shared with someone else, you may find yourself unable to download any Google Drive links from Pixiv Fanbox posts as someone else may have abused your API key.

<img src="/res/guide/gdrive_api_key/step-2.3.jpg" alt="step 2.3" style="width: 70%;">

#### Note: Below are optional steps to restrict the API key to only work with the Google Drive API (For security reasons).

Reasons: If you do not restrict the API key to only work with the Google Drive API, then anyone who gets their hands on the API key can use it to access any Google API.

1. Click on the the API key that you just created.

<img src="/res/guide/gdrive_api_key/step-2.4.jpg" alt="step 2.4" style="width: 70%;">

5. You can edit the API key name but the important thing here is under the `API restrictions`, select `Restrict key` and select `Google Drive API`.

<img src="/res/guide/gdrive_api_key/step-2.5.gif" alt="step 2.5" style="width: 70%;">

6. In the event that your API key has been leaked, you can either delete the key and generate a new one or you can click on `REGENERATE KEY` to get a new API key.

<img src="/res/guide/gdrive_api_key/step-2.6.jpg" alt="step 2.6" style="width: 70%;">

## Step 3: Set up your Google Drive API on Cultured Downloader

*You are almost there!*

1. Run [launcher.py](/src/launcher.py) or the executable and enter the command option for `Add Google Drive API Key`.

<img src="/res/guide/gdrive_api_key/step-3.1.jpg" alt="step 3.1" style="width: 70%;">

2. Paste the API key that you copied from the Google Cloud Platform Console and you are done!