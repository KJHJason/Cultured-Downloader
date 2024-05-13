# Using a Service Account

## Introduction

This guide will help you get your Service Account JSON file required for downloading files from Google Drive.

Unlike using your [OAuth2](gdrive_oauth_guide.md) credentials, a service account is an authorised bot account by Google Cloud that can be used to access Google APIs.

<- Go back to [Google Drive API Setup Guide](/doc/google_api_setup_guide.md)

### 1. Go to the `Credentials` page of your project under the `APIs & Services` tab.

<img src="/res/guide/gdrive_api_setup/step-2.1.jpg" alt="step 2.1" style="width: 70%;">

### 2. Click on `CREATE CREDENTIALS` and select `Service account`.

<img src="/res/guide/gdrive_api_setup/service_account/step-2.2.png" alt="step 2.2" style="width: 70%;">

### 3. Give the service account a name (any will do) and click `DONE`.

<img src="/res/guide/gdrive_api_setup/service_account/step-2.3.gif" alt="step 2.3" style="width: 70%;">

### 4. Click on the service account that you just created.

<img src="/res/guide/gdrive_api_setup/service_account/step-2.4.png" alt="step 2.4" style="width: 70%;">

### 5. Go to the `KEYS` tab and click on `ADD KEY` and select `Create new key`. Please ensure that the key type is set to `JSON` and click `CREATE`.

A JSON file will be downloaded and please keep it safe as anyone who gets their hands on this file can **abuse** it and access any enabled API on Google Cloud.
Please do ***NOT*** lose this file as you will have to generate a new one if you do.

<img src="/res/guide/gdrive_api_setup/service_account/step-2.5.gif" alt="step 2.5" style="width: 70%;">
