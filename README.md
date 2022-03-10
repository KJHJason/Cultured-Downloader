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
  <a href="#English">English</a>
  <a href="#Japanese">日本語</a>
</div>

---
<div name="English"></div>
This program allows you to download images from a pixiv Fanbox or Fantia post automatically without you doing the hassle of downloading them yourself.

I did this mini-project as I was tired of downloading images manually as some artists do not provide zip files...

Hence, I coded this program to automate the process of downloading images from a post via web scraping.

In the end, I spent about 8 days on this mini-project so you can expect some bugs...

Although the program has Japanese language support, most of them are translated by [DeepL](https://www.deepl.com/translator). Hence, feel free to correct any mistranslation/grammatical errors by forking it and make a pull request after correcting the translation.

## Terms of Use
1. This program, Cultured Downloader, is not liable for any damages caused. This program is meant for personal use and to save time downloading images from pixiv Fanbox and Fantia manually.
2. As a user of this program, please do not use this program to  break any of Fantia's or pixiv Fanbox's Terms of Service/Terms of Use.
3. As a user of this program, you must never share any data such as your fantia_cookies file to other people. This is not permissible as it will cause damages to the artists that you are downloading from. If you have been found to be sharing YOUR data or using OTHER people's data, this program and the developer(s) will not be liable for the damages caused but the user(s) involved will be.

## Features
* **Allow multiple URLs input**
* **3 Download Options**
    * Downloading a Fantia image url such as "https://fantia.jp/posts/1234567/post_content_photo/1234567"
      (with a simple auto detection system to detect the numbers of images to download based on the url if the user opted for it)
    * Downloading all the images in a Fantia post based on a URL such as "https://fantia.jp/posts/1234567"
    * Downloading all the images in a pixiv Fanbox post based on a URL such as "https://www.fanbox.cc/@creator/posts/1234567"

## Usage Notes
1. **This program is meant for personal use and to save time downloading images from pixiv Fanbox and Fantia manually. Please do not use this program and break any of Fantia's or pixiv Fanbox's Terms of Service/Terms of Use.**
2. If you feel unsafe providing your passwords to this program, you can proceed as a guest. However, you might not be able to download posts that requires a membership.
3. Cookies saved will be encrypted and stored in the configs folder found in your AppData LocalLow folder. However, please do not share any data with anyone as they will still be able to decrypt the encrypted cookies if you have shared the key file as well.
4. If the website design has been changed, you can expect this program to break if it is not maintained/updated.

## FAQ
1. Does this work on other OS platforms such as macOS and Linux?
    * This program has only been tested on Windows.
    * Hence, this program is unlikely to work for other platforms.

## Final Notes
1. Please remember that this was meant to be a mini-project which is meant to be used for personal use.
2. I am still an amateur in programming so if there is a bug, I may or may not be able to fix it. However, I will still do my best of course.
3. If you would like to improve on this program, you can fork this repository and make your own version and make a pull request.
4. Though, I may or may not maintain this program depending on the workload I have as a student.

---
<div name="Japanese"></div>
pixivのFanboxやFantiaの投稿から、自分で画像をダウンロードする手間を省いて、自動的に画像をダウンロードできるプログラムです。

アーティストによってはzipファイルを提供してくれないので、手動で画像をダウンロードするのに疲れてしまったので、このミニプロジェクトを行いました...

そこで、ウェブスクレイピングで記事から画像をダウンロードする処理を自動化するために、このプログラムを作りました。

結局、このミニプロジェクトに約8日間を費やしたので、いくつかのバグがあることが予想されます...

日本語に対応していますが、そのほとんどは[DeepL](https://www.deepl.com/translator)が翻訳しています。したがって、誤訳・文法的な間違いはフォークして自由に修正し、翻訳を修正した後にプルリクエストを作成してください。

## 利用規約 (誤訳があった場合は、英語版を優先して使用します。)

1. 本プログラム「Cultured Downloader」は、発生した損害について一切の責任を負いかねます。このプログラムは、個人的な使用と、pixiv FanboxとFantiaから画像を手動でダウンロードする時間を節約するためのものです。
2. 本プログラムの利用者として、Fantiaおよびpixivファンボックスの利用規約を破るような利用はしないでください。
3. 本プログラムのユーザーとして、fantia_cookiesファイルなどのデータは絶対に他人と共有しないでください。クッキーを共有することは、ダウンロード先のアーティストに損害を与えることになりますので、おやめください。自分のデータを共有したり、他人のデータを使用していることが判明した場合。このプログラムおよび開発者は損害賠償の責任を負いませんが、関係するユーザーは責任を負うものとします。

## 特徴
* **複数URLの入力を許可する**
* **3 ダウンロードオプション**
    * "https://fantia.jp/posts/1234567/post_content_photo/1234567" のようなFantiaの画像urlをダウンロードする。
      (ユーザーが選択した場合、URLに基づいてダウンロードする画像の数を検出するための簡単な自動検出システム付き)
    * "https://fantia.jp/posts/1234567" などのURLをもとに、Fantiaの投稿に含まれるすべての画像をダウンロードする。
    * "https://www.fanbox.cc/@creator/posts/1234567" などのURLをもとに、pixivファンボックスの投稿内の画像をすべてダウンロードする。

## 使用上の注意
1. **このプログラムは、個人的な利用を目的とし、pixiv FanboxおよびFantiaから画像を手動でダウンロードする時間を短縮するためのものです。このプログラムを使用して、Fantiaまたはpixiv Fanboxの利用規約を破らないようにしてください。**
2. このプログラムにパスワードを提供するのが不安な場合は、ゲストとして続行することができます。ただし、会員登録が必要な投稿はダウンロードできない場合があります。
3. 保存されたクッキーは暗号化され、AppData LocalLowフォルダー内のconfigsフォルダーに保存されます。ただし、鍵ファイルを共有している場合は、暗号化されたCookieを復号化することができますので、データを共有しないようにお願いします。
4. ウェブサイトのデザインが変更された場合、メンテナンス/更新を行わないと、このプログラムが壊れることが予想されます。

## よくある質問
1. macOSやLinuxなど、他のOSプラットフォームでも動作しますか？
    * 本プログラムはWindows上でのみ動作確認を行っています。
    * したがって、このプログラムは他のプラットフォームでは動作しない可能性があります。

## 最終ノート
1. これは個人的な使用を前提としたミニプロジェクトであることを忘れないでください。
2. 私はまだプログラミングは素人なので、もしバグがあっても直せるかもしれないし、直せないかもしれません。しかし、それでももちろんベストを尽くします。
3. このプログラムを改良したい場合は、このリポジトリをフォークして独自のバージョンを作成し、プルリクエストを行うことができます。
4. しかし、学生である私は、仕事の忙しさによってプログラムを維持することもあれば、しないこともあります。