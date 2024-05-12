<h1 align="center">
<img src="/res/cultured_downloader_logo.png" width="100px" height="100px" alt="Cultured Downloader Logo">
<br>
Cultured Downloader
</h1>

<div align="center">
    <a href="https://github.com/KJHJason/Cultured-Downloader/releases">
        <img src="https://img.shields.io/github/v/release/KJHJason/Cultured-Downloader?include_prereleases&label=Latest%20Release" />
    </a>
    <a href="https://github.com/KJHJason/Cultured-Downloader/issues">
        <img src="https://img.shields.io/github/issues/KJHJason/Cultured-Downloader" />
    </a>
    <a href="https://github.com/KJHJason/Cultured-Downloader/pulls">
        <img src="https://img.shields.io/github/issues-pr/KJHJason/Cultured-Downloader" />
    </a>
    <img src="https://img.shields.io/github/downloads/KJHJason/Cultured-Downloader/latest/total" alt="latest release downloads">
    <img src="https://img.shields.io/codeclimate/maintainability/KJHJason/Cultured-Downloader" alt="Code Climate maintainability">
</div>

<div align="center">
    <a href="./README.md">English</a>
    <a href="./README.jp.md">日本語</a>
</div>

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Star History](#star-history)
- [Running the Program](#running-the-program)
- [Terms of Use](#terms-of-use)
- [Features](#features)
- [Usage Notes](#usage-notes)
- [FAQ](#faq)
- [Final Notes](#final-notes)
- [Demo](#demo)
- [The OG Python CLI](#the-og-python-cli)

## Introduction

This program allows you to download files like images and attachment automatically without you doing the hassle of downloading them yourself from supported platforms like Fantia, Pixiv, and more!

I did this project as I was tired of downloading images manually as some artists do not provide zip files...

Hence, I coded this program to automate the process of downloading images from a post via web scraping.

In the end, I spent about a month doing developing the initial program in Python while learning concepts such as web scraping, async, threading, and more.

After learning [Go/Golang](https://go.dev) however, I decided to rewrite the program in Golang with a GUI using [wails](https://wails.io/) with [Svelte](https://svelte.dev/) as the frontend framework.

## Star History

<a href="https://star-history.com/#KJHJason/Cultured-Downloader&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=KJHJason/Cultured-Downloader&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=KJHJason/Cultured-Downloader&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=KJHJason/Cultured-Downloader&type=Date" />
  </picture>
</a>

## Running the Program

1. Running the .go files
   - Clone this repository/Download all the files in this repository.
   - Install the latest version of [Go/Golang](https://go.dev/dl/) and [Node.js](https://nodejs.org/en/download/)
   - Install the Wails CLI by running `go install github.com/wailsapp/wails/v2/cmd/wails@latest`
     - Refer to the [Wails documentation](https://wails.io/docs/next/gettingstarted/installation#installing-wails) if there is any issues faced when installing the Wails CLI. 
   - Run `wails build` in the root directory of this repository to build the binary and run the program.
     - Alternatively, you can run `wails dev` to run the program in development mode. 

2. Running the executable file
   - Download the latest Cultured Downloader executable file (.exe) from the [releases page](https://github.com/KJHJason/Cultured-Downloader/releases)
   - Once downloaded, you can do an integrity check for security reasons by comparing the SHA256 hash of the downloaded executable file the hash provided in the release notes.
   - Finally, you can enjoy running the program!

## Terms of Use

1. This program, Cultured Downloader, is not liable for any damages caused. This program is meant for personal use and to save time downloading images from the various platforms manually.

2. As a user of this program, please do not use this program to break any of the platform's Terms of Service/Terms of Use.

3. As a user of this program, you must never share any data such as your cookie files to other people. This is not permissible as it may cause damages to the artists that you are downloading from. If you have been found to be sharing YOUR data or using OTHER people's data, this program and the developer(s) will not be liable for the damages caused but the user(s) involved will be.

4. By using this program, you agree to the terms and conditions stated above. If you do not agree to the terms and conditions, you are not permitted to for the repository, edit the source code, or use this program.

## Features

- Allow saving of the necessary data like session cookies for future downloads
- Download images and attachments from the following:
  - Fantia
  - Pixiv Fanbox
  - Pixiv
  - Kemono
- Concurrent downloads for faster downloads
  - Note: This is more prominent on Fantia as the other platforms have rate limits or throttles the download speed.
- Download GDrive links from posts on:
  - Fantia
  - Pixiv Fanbox
  - Kemono
  - Note: Requires an API key from Google Cloud Platform for GDrive downloads to work.
    - Refer to my [guide](doc/google_api_key_guide.md) if unsure.
- Detect other URL(s) like MEGA, Dropbox, etc. and logs them for your reference
- Detect passwords for attachments like .zip files and logs them for your reference
- using [FFmpeg](https://ffmpeg.org/) to convert Pixiv Ugoira to user-friendly formats like .gif, .apng, .webp, .webm, and .mp4

## Usage Notes

1. This program is meant for personal use and to save time downloading images from the various platforms manually. Please do not use this program and break any of the platform's Terms of Service/Terms of Use.

2. If you feel unsafe entering your session cookie information into the program, you will not be able to proceed and download. However, please rest assured as the program will never send anything sensitive out of your system!

3. Sensitive data, such as your session cookie, can be encrypted at rest by providing a master password. However, please refrain from sharing the encrypted data with anyone to be extra safe!
   - Note: The program uses [XChaCha20-Poly1305](https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-xchacha-03) encryption to encrypt the sensitive data.

4. If the platform's frontend design or API has been changed, you can expect this program to break if it is not maintained/updated. In this case, please raise an [issue](https://github.com/KJHJason/Cultured-Downloader/issues) and I will take it a look at it and hopefully fix it as soon as possible.

## FAQ

1. Does this work on other OS platforms such as macOS and Linux?
   - This program has only been tested on Windows and Linux (Ubuntu). However, it should work on other Linux distros and macOS as well.
2. The program suddenly closes/crashes! What should I do?
   - This is due to how error handling in Golang works, when a fatal error occurs, the program will `panic` and closes itself.
   - However, please raise an [issue](https://github.com/KJHJason/Cultured-Downloader/issues) with the steps to reproduce the error and I will do my best to fix it.

## Final Notes

1. Please remember that is meant to be used for personal use.
2. If there is a bug, you can raise an [issue](https://github.com/KJHJason/Cultured-Downloader/issues) and I will do my best to fix it. Otherwise, you can fork this repository and make a [pull request](https://github.com/KJHJason/Cultured-Downloader/pulls) to fix the bug if you would like to do so.
3. If you would like to improve on this program, you can fork this repository and do the necessary changes and make a [pull request](https://github.com/KJHJason/Cultured-Downloader/pulls). I will then review it and merge it I feel that it is a good contribution.
4. Please consider supporting this project by [buying me a coffee](https://ko-fi.com/dratornic) or [sponsoring me](https://github.com/sponsors/KJHJason)!
   - Your contribution would help ensure the sustainability of this project. Thank you for reading &lt;3

## Demo

<div align="center">
  <p>Downloading files from a Fantia post and managing the Download Queues</p>
  <p><img width="650px" alt="downloading Fantia demo and download queue demo" src="res/fantia-and-download-queue.gif"></p>
  <p>General Settings</p>
  <p><img width="650px" alt="general settings" src="res/general-settings.png"></p>
  <p>Preferences</p>
  <p><img width="650px" alt="preferences settings" src="res/preferences.png"></p>
  <p>Advanced Settings</p>
  <p><img width="650px" alt="advanced settings" src="res/advanced-settings.png"></p>
</div>

## The OG Python CLI

<div align="center">
  <p>Menu</p>
  <p><img width="500px" alt="menu demo" src="res/old/menu.jpg"></p>
  <p>Downloading files from a post page URL</p>
  <p><img width="650px" alt="downloading posts demo" src="res/old/post-download.gif"></p>
  <p>Downloading files from multiple posts from multiple creators</p>
  <p><img width="650px" alt="downloading multiple posts demo" src="res/old/creator-page-downloads.gif"></p>
</div>
