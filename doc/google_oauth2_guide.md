# Google OAuth2 Guide

## Introduction

This guide will help you to get your Google OAuth2 credentials. 
You will need the credentials to use the Google Drive API to download files from Google Drive.

*You can **ignore** this guide if you do not wish to download any Google Drive links from Pixiv Fanbox posts.*

### Step 1: Create a Google Cloud Platform Project and enable the Google Drive API

1. Go to the [Google Cloud Platform Console](https://console.cloud.google.com/).

<img src="/res/guide/gcp-oauth2/step-1.1.jpg" alt="step 1.1" style="width: 70%;">

2. Create a new project.
3. Give the project a name (any will do) and click **Create**.

<img src="/res/guide/gcp-oauth2/step-1.2-1.3.gif" alt="step 1.2 to 1.3" style="width: 70%;">

4. **IMPORTANT**: Please make sure to enable [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com) for the project. Otherwise, you will get a 403 Forbidden error when calling the Google Drive API.

<img src="/res/guide/gcp-oauth2/step-1.4.jpg" alt="step 1.4" style="width: 70%;">

### Step 2: Configure OAuth2 Consent Screen

1. Go to the [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent) page under the **APIs & Services** section of the side navigation bar.

<img src="/res/guide/gcp-oauth2/step-2.1.jpg" alt="step 2.1" style="width: 70%;">

2. Select "**External**" for the user type.

<img src="/res/guide/gcp-oauth2/step-2.2.jpg" alt="step 2.2" style="width: 70%;">

1. Enter a name such as `Cultured Downloader` under the **App name** field.
2. Select your own email address under the **User support email** field.
3. Enter your own email address under the **Developer contact information** field and click **SAVE AND CONTINUE**
4. Continue clicking **SAVE AND CONTINUE** until you reach the **Test users** page.

<img src="/res/guide/gcp-oauth2/step-2.3-2.5.gif" alt="step 2.3 to 2.5" style="width: 70%;">

7. Under the **Test users** page, click **ADD USERS** and enter your own email address.
8. Once you are on the **Summary** page, click **BACK TO DASHBOARD** on the bottom of the page.

<img src="/res/guide/gcp-oauth2/step-2.7.gif" alt="step 2.7" style="width: 70%;">

### Step 3: Create OAuth2 Credentials

1. Go to the **Credentials** page of your project under the **APIs & Services** tab.

<img src="/res/guide/gcp-oauth2/step-3.1.jpg" alt="step 3.1" style="width: 70%;">

2. Click on **CREATE CREDENTIALS** and select **OAuth client ID**.

<img src="/res/guide/gcp-oauth2/step-3.2.jpg" alt="step 3.2" style="width: 70%;">

3. Under the **Application type** section, select **Web application**.

<img src="/res/guide/gcp-oauth2/step-3.3.jpg" alt="step 3.3" style="width: 70%;">

4. For the **Name** field, enter any name such as `cultured-downloader`.
5. Under the **Authorized redirect URIs** section, enter the following URL: `http://localhost:8080/`
6. Click on **CREATE** at the bottom of the page and you will be redirected to the **Credentials** page.

<img src="/res/guide/gcp-oauth2/step-3.4-3.6.jpg" alt="step 3.4 to 3.6" style="width: 70%;">

7. After being redirected, you should see a prompt, click on the **Download JSON** button on the prompt.
   1. Alternatively, under the **OAuth 2.0 client IDs** section, click on the download icon on the right side of the client ID you just created.

Prompt:

<img src="/res/guide/gcp-oauth2/step-3.7.png" alt="step 3.7" style="width: 70%;">

Alternative:

<img src="/res/guide/gcp-oauth2/step-3.7-alternative.jpg" alt="step 3.7 alternative" style="width: 70%;">

### Step 4: Setup Google OAuth2 on Cultured Downloader

*You are almost there!*

1. Run [launcher.py](/src/launcher.py) or the executable and enter the command option for **Configure Google OAuth2 for Google Drive API**.
   - If facing any issues due to cross-platform issues, please refer to the documentation [here](https://github.com/KJHJason/Cultured-Downloader/blob/main/doc/google_oauth_helper_script.md) for running [google_oauth.py](https://github.com/KJHJason/Cultured-Downloader/blob/main/src/helper/google_oauth.py) manually to set up Google OAuth2.
2. Copy the contents of the downloaded JSON file and paste it when asked for the **client secret JSON**.

<img src="/res/guide/gcp-oauth2/step-4.1-4.2.jpg" alt="step 4.1 to 4.2" style="width: 70%;">

3. A new terminal and a new tab on your web browser should have opened.
   1. If the new tab on your web browser did not open, copy the URL from the terminal and paste it on your web browser.
   2. You can also close the newly opened terminal if you wish to abort the process.

<img src="/res/guide/gcp-oauth2/step-4.3.jpg" alt="step 4.3" style="width: 70%;">

4. Sign in as usual and click **Continue** when prompted.
5. Once you signed in, you should see a message saying **The authentication flow has completed. You may close this window.** on your web browser.
6. Cultured Downloader will handle the rest and you are done!