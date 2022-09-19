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
</div>

<div align="center">
  <a href="#introduction">English</a>
  <a href="#お知らせ">日本語</a>
</div>

---

## Table of Contents/目次
[English](#introduction)
  - [Introduction](#introduction)
  - [Running the Python File](#running-the-python-file)
  - [Terms of Use](#terms-of-use)
  - [Features](#features)
  - [Usage Notes](#usage-notes)
  - [FAQ](#faq)
  - [Final Notes](#final-notes)
  - [Screenshots](#screenshots)
---

## Introduction
This program allows you to download images from a pixiv Fanbox or Fantia post automatically without you doing the hassle of downloading them yourself.

I did this project as I was tired of downloading images manually as some artists do not provide zip files...

Hence, I coded this program to automate the process of downloading images from a post via web scraping.

In the end, I spent about 2-4 weeks learning concepts such as web scraping, async, threading, and more.

## Running the Python File
- Download all the files in this repository.
- Install [Python 3.9.0 or above](https://www.python.org/downloads/)
- Install all dependencies by running the command below:
  ```
  pip install -r requirements.txt
  ```
- Run cultured_downloader.py and enjoy!

## Terms of Use
1. This program, Cultured Downloader, is not liable for any damages caused. This program is meant for personal use and to save time downloading images from pixiv Fanbox and Fantia manually.

2. As a user of this program, please do not use this program to  break any of Fantia's or pixiv Fanbox's Terms of Service/Terms of Use.

3. As a user of this program, you must never share any data such as your cookie files to other people. This is not permissible as it may cause damages to the artists that you are downloading from. If you have been found to be sharing YOUR data or using OTHER people's data, this program and the developer(s) will not be liable for the damages caused but the user(s) involved will be.

## Features
* **Allow multiple URLs input**
* **Allow downloads of attachments such as videos, psd, etc.**
* **Allow downloads of gdrive links (for pixiv Fanbox only)**
* **4 Download Options**
    * Downloading all the images or attachment files (videos, psd, etc.) in a Fantia post based on a URL such as "https://fantia.jp/posts/1234567"
    * Downloading all the images or attachment files (videos, psd, etc.) in a pixiv Fanbox post based on a URL such as "https://www.fanbox.cc/@creator_name/posts/1234567"
    * Downloading images or attachment files (videos, psd, etc.) from Fantia's all posts page URL such as "https://fantia.jp/fanclubs/1234/posts"
    * Downloading images or attachment files (videos, psd, etc.) from pixiv Fanbox's all posts page URL such as "https://www.fanbox.cc/@creator_name/posts"<br>
      (The user will then be asked to specify the page number. For example, "1-3" to specify page 1 to 3. In another instance, the user can enter "4" to specify page 4 only.)

## Usage Notes
1. **This program is meant for personal use and to save time downloading images from pixiv Fanbox and Fantia manually. Please do not use this program and break any of Fantia's or pixiv Fanbox's Terms of Service/Terms of Use.**

2. If you feel unsafe signing in to this program with your accounts, you can proceed as a guest. However, you might not be able to download posts that requires a membership.

3. The cookies saved will be encrypted and stored in the configs folder. However, please do not share any data with anyone as they may still be able to decrypt the encrypted cookies if you have shared the key file as well.
   * If you have saved your key on Cultured Downloader API, you *should* be fine but it still not recommended to share your data with anyone as they might be able to decrypt the encrypted cookies and hijack your account.

4. If the website design has been changed, you can expect this program to break if it is not maintained/updated. In this case, please raise an issue and I will take it a look at it and hopefully fix it as soon as possible.

## FAQ
1. Does this work on other OS platforms such as macOS and Linux?
    * This program has only been tested on Windows and Linux. However, it should work on macOS as well.

## Final Notes
1. Please remember that this was meant to be a mini-project which is meant to be used for personal use.
2. I am still an amateur in programming so if there is a bug, you can raise an issue and I will do my best to fix it. Otherwise, you can fork this repository and make a pull request to fix the bug if you would like to do so.
3. If you would like to improve on this program, you can fork this repository and do the necessary changes and make a pull request. I will then review it and merge it I feel that it is a good contribution.
4. Though, I may or may not maintain this program depending on the workload I have as a student.

## Screenshots

<div align="center">
  <p>Soon to be added!</p>
</div>

---

## お知らせ

残念ながら、翻訳するとしたら、ほとんどDeepLを使うことになるので、日本語のサポートは外しました。

ただし、このプログラムを翻訳したい方は、リポジトリへのコントリビューションを歓迎します。