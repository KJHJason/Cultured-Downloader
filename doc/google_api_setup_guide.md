# Google Drive API Guide

## Introduction

This guide will help you get your Google Drive API key required for downloading files from Google Drive.

*You can `disregard` this guide if you prefer not to download any Google Drive links or if you're only interested in downloading posts from Pixiv*

## Step 1: Create a Google Cloud Platform Project and enable the Google Drive API

1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/).

<img src="/res/guide/gdrive_api_setup/step-1.1.jpg" alt="step 1.1" style="width: 70%;">

2. Create a new project.
3. Give the project a name (any will do) and click `Create`.

<img src="/res/guide/gdrive_api_setup/step-1.2-1.3.gif" alt="step 1.2 to 1.3" style="width: 70%;">

4. `IMPORTANT`: Please make sure to enable [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com) for the project. Otherwise, you will get a 403 Forbidden error when calling the Google Drive API.

<img src="/res/guide/gdrive_api_setup/step-1.4.jpg" alt="step 1.4" style="width: 70%;">

## Choose your preferred method

1. [Using an API Key](#using-an-api-key)
   - Much easier to setup but more likely to be get flagged for abuse by Google (will be unable to download any Google Drive links with the API key for a while)
2. [Using a Service Account](#using-a-service-account)
   - Slighly more complicated to setup but less likely to get flagged for abuse by Google.

## Using an API Key

1. Go to the `Credentials` page of your project under the `APIs & Services` tab.

<img src="/res/guide/gdrive_api_setup/step-2.1.jpg" alt="step 2.1" style="width: 70%;">

2. Click on `CREATE CREDENTIALS` and select `API key`.

<img src="/res/guide/gdrive_api_setup/api_key/step-2.2.jpg" alt="step 2.2" style="width: 70%;">

3. A prompt will appear with your API key. Copy the key as we will have to paste it when running the Cultured Downloader program.
   1. Please do ***NOT*** share your API key with anyone.
      - Note that you have a limit of 20,000 requests per every 100 seconds or 1 billion requests per day.
        - Usage limits reference: [https://developers.google.com/drive/api/guides/limits](https://developers.google.com/drive/api/guides/limits)
      - Hence, if it is shared with someone else, you may find yourself unable to download any Google Drive links from Pixiv Fanbox posts as someone else may have abused your API key.

<img src="/res/guide/gdrive_api_setup/api_key/step-2.3.jpg" alt="step 2.3" style="width: 70%;">

#### Note: Below are optional steps to restrict the API key to only work with the Google Drive API (For security reasons).

Reasons: If you do not restrict your API key to only work with Google Drive API, then anyone who gets their hands on your API key can **abuse** it and access any enabled API on Google Cloud.

4. Click on the the API key that you just created.

<img src="/res/guide/gdrive_api_setup/api_key/step-2.4.jpg" alt="step 2.4" style="width: 70%;">

5. You can edit the API key name but the important thing here is under the `API restrictions`, select `Restrict key` and select `Google Drive API`.

<img src="/res/guide/gdrive_api_setup/api_key/step-2.5.gif" alt="step 2.5" style="width: 70%;">

6. In the event that your API key has been leaked, you can either delete the key and generate a new one or you can click on `REGENERATE KEY` to get a new API key.

<img src="/res/guide/gdrive_api_setup/api_key/step-2.6.jpg" alt="step 2.6" style="width: 70%;">

## Using a Service Account

1. Go to the `Credentials` page of your project under the `APIs & Services` tab.

<img src="/res/guide/gdrive_api_setup/step-2.1.jpg" alt="step 2.1" style="width: 70%;">

2. Click on `CREATE CREDENTIALS` and select `Service account`.

<img src="/res/guide/gdrive_api_setup/service_account/step-2.2.png" alt="step 2.2" style="width: 70%;">

3. Give the service account a name (any will do) and click `CREATE`.

<img src="/res/guide/gdrive_api_setup/service_account/step-2.3.gif" alt="step 2.3" style="width: 70%;">

4. Click on the service account that you just created.

<img src="/res/guide/gdrive_api_setup/service_account/step-2.4.png" alt="step 2.4" style="width: 70%;">

5. Go to the `KEYS` tab and click on `ADD KEY` and select `Create new key`. Please ensure that the key type is set to `JSON` and click `CREATE`.

A JSON file will be downloaded and please keep it safe as anyone who gets their hands on this file can **abuse** it and access any enabled API on Google Cloud.
Please do ***NOT*** lose this file as you will have to generate a new one if you do.

<img src="/res/guide/gdrive_api_setup/service_account/step-2.5.gif" alt="step 2.5" style="width: 70%;">
