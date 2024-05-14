# Using an API Key

## Introduction

This guide will help you get your API Key required for downloading files from Google Drive.

The reason why using an API key is likely to be flagged for abuse by Google is because it is unauthenticated and can be easily leaked or shared with others.

<- Go back to [GCP Setup Guide](/doc/gcp_setup_guide.md)

### 1. Go to the `Credentials` page of your project under the `APIs & Services` tab.

<img src="/res/guide/gdrive_api_setup/step-2.1.jpg" alt="step 2.1" style="width: 70%;">

### 2. Click on `CREATE CREDENTIALS` and select `API key`.

<img src="/res/guide/gdrive_api_setup/api_key/step-2.2.jpg" alt="step 2.2" style="width: 70%;">

### 3. A prompt will appear with your API key. Copy the key as we will have to paste it when running the Cultured Downloader program.

   1. Please do ***NOT*** share your API key with anyone.
      - Note that you have a limit of 20,000 requests per every 100 seconds or 1 billion requests per day.
        - Usage limits reference: [https://developers.google.com/drive/api/guides/limits](https://developers.google.com/drive/api/guides/limits)
      - Hence, if it is shared with someone else, you may find yourself unable to download any Google Drive links from Pixiv Fanbox posts as someone else may have abused your API key.

<img src="/res/guide/gdrive_api_setup/api_key/step-2.3.jpg" alt="step 2.3" style="width: 70%;">

### Note: Below are optional steps to restrict the API key to only work with the Google Drive API (For security reasons).

Reasons: If you do not restrict your API key to only work with Google Drive API, then anyone who gets their hands on your API key can **abuse** it and access any enabled API on Google Cloud.

### 4. Click on the the API key that you just created.

<img src="/res/guide/gdrive_api_setup/api_key/step-2.4.jpg" alt="step 2.4" style="width: 70%;">

### 5. You can edit the API key name but the important thing here is under the `API restrictions`, select `Restrict key` and select `Google Drive API`.

<img src="/res/guide/gdrive_api_setup/api_key/step-2.5.gif" alt="step 2.5" style="width: 70%;">

### 6. In the event that your API key has been leaked, you can either delete the key and generate a new one or you can click on `REGENERATE KEY` to get a new API key.

<img src="/res/guide/gdrive_api_setup/api_key/step-2.6.jpg" alt="step 2.6" style="width: 70%;">
