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
  <a href="#イントロダクション">日本語</a>
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

[日本語](#イントロダクション)
  - [イントロダクション](#イントロダクション)
  - [Pythonファイルの実行](#pythonファイルの実行)
  - [利用規約](#利用規約)
  - [特徴](#特徴)
  - [使用上の注意](#使用上の注意)
  - [よくある質問](#よくある質問)
  - [最終ノート](#最終ノート)
  - [スクリーンショット](#スクリーンショット)

---

## Introduction
This program allows you to download images from a pixiv Fanbox or Fantia post automatically without you doing the hassle of downloading them yourself.

I did this mini-project as I was tired of downloading images manually as some artists do not provide zip files...

Hence, I coded this program to automate the process of downloading images from a post via web scraping.

In the end, I spent about 8 days on this mini-project so you can expect some bugs...

Although the program has Japanese language support, most of them are translated by [DeepL](https://www.deepl.com/translator). Hence, feel free to correct any mistranslation/grammatical errors by forking it and make a pull request after correcting the translation.

## Running the Python File
- Download all the files in this repository.
- Install [Python 3.8.X or above](https://www.python.org/downloads/)
- Install all dependencies by running the command below:
  ```
  pip install -r requirements.txt
  ```
- Run CulturedDownloader.py and enjoy!

## Terms of Use
1. This program, Cultured Downloader, is not liable for any damages caused. This program is meant for personal use and to save time downloading images from pixiv Fanbox and Fantia manually.
2. As a user of this program, please do not use this program to  break any of Fantia's or pixiv Fanbox's Terms of Service/Terms of Use.
3. As a user of this program, you must never share any data such as your fantia_cookies file to other people. This is not permissible as it will cause damages to the artists that you are downloading from. If you have been found to be sharing YOUR data or using OTHER people's data, this program and the developer(s) will not be liable for the damages caused but the user(s) involved will be.

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
2. If you feel unsafe providing your passwords to this program, you can proceed as a guest. However, you might not be able to download posts that requires a membership.
3. Cookies saved will be encrypted and stored in the configs folder found in your AppData Roaming folder. However, please do not share any data with anyone as they will still be able to decrypt the encrypted cookies if you have shared the key file as well.
4. If the website design has been changed, you can expect this program to break if it is not maintained/updated.

## FAQ
1. Does this work on other OS platforms such as macOS and Linux?
    * This program has only been tested on Windows.
    * However, I have added support for macOS and Linux but have yet to test them as I do not have a Linux or a macOS system.

## Final Notes
1. Please remember that this was meant to be a mini-project which is meant to be used for personal use.
2. I am still an amateur in programming so if there is a bug, I may or may not be able to fix it. However, I will still do my best of course.
3. If you would like to improve on this program, you can fork this repository and make your own version and make a pull request.
4. Though, I may or may not maintain this program depending on the workload I have as a student.

## Screenshots
<div align="center">
  <p>Menu</p>
  <p><img width="500px" alt="menu demo" src="/res/en_menu.jpg"></p>
  <p>Downloading files from a post page URL</p>
  <p><img width="650px" alt="downloading posts demo" src="/res/en_post_download.jpg"></p>
  <p>Downloading files from multiple posts from an all post page URL</p>
  <p><img width="650px" alt="downloading multiple posts demo" src="/res/en_all_posts_download.jpg"></p>
</div>

---

## イントロダクション
pixivのFanboxやFantiaの投稿から、自分で画像をダウンロードする手間を省いて、自動的に画像をダウンロードできるプログラムです。

アーティストによってはzipファイルを提供してくれないので、手動で画像をダウンロードするのに疲れてしまったので、このミニプロジェクトを行いました...

そこで、ウェブスクレイピングで記事から画像をダウンロードする処理を自動化するために、このプログラムを作りました。

結局、このミニプロジェクトに約8日間を費やしたので、いくつかのバグがあることが予想されます...

日本語に対応していますが、そのほとんどは[DeepL](https://www.deepl.com/translator)が翻訳しています。したがって、誤訳・文法的な間違いはフォークして自由に修正し、翻訳を修正した後にプルリクエストを作成してください。

## Pythonファイルの実行
- リポジトリにあるすべてのファイルをダウンロードしてください。
- [Python 3.8.X](https://www.python.org/downloads/)以上をインストールする
- 以下のコマンドを実行し、すべての依存関係をインストールします:
  ```
  pip install -r requirements.txt
  ```
- CulturedDownloader.pyを実行して、お楽しみください。

## 利用規約 
(誤訳があった場合は、英語版を優先して使用します。)
1. 本プログラム「Cultured Downloader」は、発生した損害について一切の責任を負いかねます。このプログラムは、個人的な使用と、pixiv FanboxとFantiaから画像を手動でダウンロードする時間を節約するためのものです。
2. 本プログラムの利用者として、Fantiaおよびpixivファンボックスの利用規約を破るような利用はしないでください。
3. 本プログラムのユーザーとして、fantia_cookiesファイルなどのデータは絶対に他人と共有しないでください。クッキーを共有することは、ダウンロード先のアーティストに損害を与えることになりますので、おやめください。自分のデータを共有したり、他人のデータを使用していることが判明した場合。このプログラムおよび開発者は損害賠償の責任を負いませんが、関係するユーザーは責任を負うものとします。

## 特徴
* **複数URLの入力ができます**
* **ビデオ、psdなどの添付ファイルのダウンロードができます**
* **gdriveのリンクのダウンロードができます（pixiv Fanboxのみ）**
* **4 ダウンロードオプション**
    * "https://fantia.jp/posts/1234567" などのURLをもとに、Fantiaの投稿に含まれるすべての画像や添付ファイルをダウンロードする。
    * "https://www.fanbox.cc/@creator_name/posts/1234567" などのURLをもとに、pixivファンボックスの投稿内の画像や添付ファイルをすべてダウンロードする。
    * Fantiaの全投稿ページURLの "https://fantia.jp/fanclubs/1234/posts" などから画像や添付ファイルをダウンロードすることができます。
    * pixivファンボックスの全投稿ページURLの "https://www.fanbox.cc/@creator_name/posts" などから画像や添付ファイルをダウンロードすることができます。<br>
      (次に、ページ番号を指定するように指示されます。例えば、"1-3 "と入力すると1ページから3ページが指定され、"4 "と入力すると4ページだけが指定されます。)

## 使用上の注意
1. **このプログラムは、個人的な利用を目的とし、pixiv FanboxおよびFantiaから画像を手動でダウンロードする時間を短縮するためのものです。このプログラムを使用して、Fantiaまたはpixiv Fanboxの利用規約を破らないようにしてください。**
2. このプログラムにパスワードを提供するのが不安な場合は、ゲストとして続行することができます。ただし、会員登録が必要な投稿はダウンロードできない場合があります。
3. 保存されたクッキーは暗号化され、AppData Roamingフォルダー内のconfigsフォルダーに保存されます。ただし、鍵ファイルを共有している場合は、暗号化されたCookieを復号化することができますので、データを共有しないようにお願いします。
4. ウェブサイトのデザインが変更された場合、メンテナンス/更新を行わないと、このプログラムが壊れることが予想されます。

## よくある質問
1. macOSやLinuxなど、他のOSプラットフォームでも動作しますか？
    * 本プログラムはWindows上でのみ動作確認を行っています。
    * ただし、macOSとLinuxのサポートを追加しましたが、LinuxやmacOSのシステムを持っていないので、まだテストしていません。

## 最終ノート
1. これは個人的な使用を前提としたミニプロジェクトであることを忘れないでください。
2. 私はまだプログラミングは素人なので、もしバグがあっても直せるかもしれないし、直せないかもしれません。しかし、それでももちろんベストを尽くします。
3. このプログラムを改良したい場合は、このリポジトリをフォークして独自のバージョンを作成し、プルリクエストを行うことができます。
4. しかし、学生である私は、仕事の忙しさによってプログラムを維持することもあれば、しないこともあります。

## スクリーンショット
<div align="center">
  <p>メニュー</p>
  <p><img width="500px" alt="メニューデモ" src="/res/jp_menu.jpg"></p>
  <p>投稿ページのURLからファイルをダウンロードする</p>
  <p><img width="650px" alt="投稿ダウンロードのデモ" src="/res/jp_post_download.jpg"></p>
  <p>全投稿ページのURLから複数の投稿のファイルをダウンロードする</p>
  <p><img width="650px" alt="複数記事のダウンロードデモ" src="/res/jp_all_posts_download.jpg"></p>
</div>