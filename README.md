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
    * Downloading all the images in a Fanbox post based on a URL such as "https://www.fanbox.cc/@creator/posts/1234567"

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
