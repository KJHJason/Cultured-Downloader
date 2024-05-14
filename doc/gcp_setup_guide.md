# Google Cloud Platform Setup Guide

## Introduction

This guide will help you to create a Google Cloud Platform (GCP) project in order to get your API Key or Service Account JSON file required for downloading files from Google Drive.

## Step 1: Create a Google Cloud Platform Project and enable the Google Drive API

1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/).

<img src="/res/guide/gdrive_api_setup/step-1.1.jpg" alt="step 1.1" style="width: 70%;">

2. Create a new project.
3. Give the project a name (any will do) and click `Create`.

<img src="/res/guide/gdrive_api_setup/step-1.2-1.3.gif" alt="step 1.2 to 1.3" style="width: 70%;">

4. `IMPORTANT`: Please make sure to enable [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com) for the project. Otherwise, you will get a 403 Forbidden error when calling the Google Drive API.

<img src="/res/guide/gdrive_api_setup/step-1.4.jpg" alt="step 1.4" style="width: 70%;">

## Choose your preferred method

1. [Using an API Key](gdrive_api_key_guide.md)
   - Much easier to setup but more likely to be get flagged for abuse by Google (will be unable to download any Google Drive links with the API key for a while)
2. [Using a Service Account](gdrive_service_acc_guide.md)
   - Slighly more complicated to setup but less likely to get flagged for abuse by Google.
3. [Using OAuth 2.0](google_oauth_guide.md)
   - Most complicated to setup but least likely to get flagged for abuse by Google.
