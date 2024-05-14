# Google OAuth2 Guide

## Introduction

This guide will help you to get your Google OAuth2 credentials for GDrive. 

Unlike service accounts which are authorised bot accounts, the obtained OAuth2 credentials are tied to your Google account and can be used to access Google APIs.

This means that the requests made using these credentials are made on behalf of your Google account which is less likely to be flagged for abuse by Google.

However, this would mean that if your OAuth2 credentials are leaked, the person who has access to them can use them to **view and download all your uploaded files on GDrive**.

Hence, it is important to keep your OAuth2 credentials safe and not share them with anyone.

<- Go back to [Google Drive API Setup Guide](/doc/google_api_setup_guide.md)

### Step 1: Configure OAuth2 Consent Screen

1. Go to the [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent) page under the **APIs & Services** section of the side navigation bar.

<img src="/res/guide/gdrive_api_setup/oauth2/step-2.1.jpg" alt="step 2.1" style="width: 70%;">

2. Select "**External**" for the user type.

<img src="/res/guide/gdrive_api_setup/oauth2/step-2.2.jpg" alt="step 2.2" style="width: 70%;">

1. Enter a name such as `Cultured Downloader` under the **App name** field.
2. Select your own email address under the **User support email** field.
3. Enter your own email address under the **Developer contact information** field and click **SAVE AND CONTINUE**
4. Continue clicking **SAVE AND CONTINUE** until you reach the **Test users** page.

<img src="/res/guide/gdrive_api_setup/oauth2/step-2.3-2.5.gif" alt="step 2.3 to 2.5" style="width: 70%;">

7. Under the **Test users** page, click **ADD USERS** and enter your own email address.
8. Once you are on the **Summary** page, click **BACK TO DASHBOARD** on the bottom of the page.

<img src="/res/guide/gdrive_api_setup/oauth2/step-2.7.gif" alt="step 2.7" style="width: 70%;">

### Step 2: Create OAuth2 Credentials

1. Go to the **Credentials** page of your project under the **APIs & Services** tab.

<img src="/res/guide/gdrive_api_setup/oauth2/step-3.1.jpg" alt="step 3.1" style="width: 70%;">

2. Click on **CREATE CREDENTIALS** and select **OAuth client ID**.

<img src="/res/guide/gdrive_api_setup/oauth2/step-3.2.jpg" alt="step 3.2" style="width: 70%;">

3. Under the **Application type** section, select **Web application**.

<img src="/res/guide/gdrive_api_setup/oauth2/step-3.3.jpg" alt="step 3.3" style="width: 70%;">

4. For the **Name** field, enter any name such as `cultured-downloader`.
5. Under the **Authorized redirect URIs** section, enter the following URL: `http://localhost:8080/`
6. Click on **CREATE** at the bottom of the page and you will be redirected to the **Credentials** page.

<img src="/res/guide/gdrive_api_setup/oauth2/step-3.4-3.6.jpg" alt="step 3.4 to 3.6" style="width: 70%;">

7. After being redirected, you should see a prompt, click on the **Download JSON** button on the prompt.
   1. Alternatively, under the **OAuth 2.0 client IDs** section, click on the download icon on the right side of the client ID you just created.

Prompt:

<img src="/res/guide/gdrive_api_setup/oauth2/step-3.7.png" alt="step 3.7" style="width: 70%;">

Alternative:

<img src="/res/guide/gdrive_api_setup/oauth2/step-3.7-alternative.jpg" alt="step 3.7 alternative" style="width: 70%;">

### Step 3: Setup Google OAuth2 on Cultured Downloader

*You are almost there!*

1. Upload the downloaded JSON file to Cultured Downloader in the Advanced Settings.

<img src="/res/guide/gdrive_api_setup/oauth2/step-4.1.png" alt="step 4.1" style="width: 70%;">

2. If you receive a prompt indicating that Windows Defender Firewall has blocked some features of the program, you can click either "Allow" or "Cancel" (on Windows 11). It doesn't matter, as it's just the OAuth2 localhost server that I developed, attaching itself to port localhost:8080 to capture your OAuth2 code during the OAuth callback for a better user experience!

3. A new tab should have opened on your default web browser, sign in with the account that you have previously added into the list of Test User on GCP.
   - Note: If you have accidentally closed the OAuth2 tab, you can click on the **Verify** button on Cultured Downloader to open the OAuth2 tab again. 

<img src="/res/guide/gdrive_api_setup/oauth2/step-4.2.png" alt="step 4.2" style="width: 70%;">

4. Once you have signed in, make sure to allow the permissions requested.

<img src="/res/guide/gdrive_api_setup/oauth2/step-4.3.png" alt="step 4.3" style="width: 70%;">

5. You should see a message saying "**The authentication flow has completed. You may close this window.**" on your web browser.

<img src="/res/guide/gdrive_api_setup/oauth2/step-4.4.png" alt="step 4.4" style="width: 70%;">

6. Go back to the program and click **Verify** to check if the OAuth2 credentials have been successfully set up. If it's successful, you're done!
   - If there are any difficulties or problems along the way, you can create a new [issue](https://github.com/KJHJason/Cultured-Downloader/issues) on the GitHub repository. I will do my best to assist you! 

<img src="/res/guide/gdrive_api_setup/oauth2/step-4.5.png" alt="step 4.5" style="width: 70%;">
