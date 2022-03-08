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

In the end, I spent about 6 days on this mini-project so you can expect some bugs...

## Disclaimers
1. This program, Cultured Downloader, is not liable for any damages caused. 
   This program is meant for personal use and to save time downloading images from pixiv Fanbox and Fantia manually.
2. This program requires the user to login upon running this program and if the user is not logged in, he/she will not be able to download any images that requires a membership as to support the artist.
3. As a user of this program, you must never share any data such as config.json to other people.
   If you have been found to be sharing YOUR data or using OTHER people's data, this program and the developer(s) will not be liable but the user(s) involved will be.
4. Although the program has Japanese language support, most of them are translated by [DeepL](https://www.deepl.com/translator). Hence, feel free to correct any mistranslation/grammatical errors by forking it and make a pull request after correcting the translation.

## Features
* **Allow multiple URLs input**
* **3 Download Options**
    * Downloading a Fantia image url such as "https://fantia.jp/posts/1234567/post_content_photo/1234567"
    * Downloading all the images in a Fantia post based on a URL such as "https://fantia.jp/posts/1234567"
    * Downloading all the images in a Fanbox post based on a URL such as "https://www.fanbox.cc/@creator/posts/1234567"

## Usage Notes
1. Frequent logins to pixiv may render the program useless as they have a bot detection algorithm. In this case, please use run the pixiv_manual_login program to save the cookie needed for the login session, it will also speed up the login process.
2. By saving the cookie needed for pixiv login session, you must not share the cookie with anyone as they can gain access to your pixiv account without needing your pixiv account credentials.
3. Despite testing the program, the logins have a high failure rate, so please be patient and try again if you are unable to login.
4. If you feel unsafe providing your passwords to this program, you can proceed as a guest. However, you might not be able to download posts that requires a membership.
5. Passwords provided will be encrypted and stored in a config.json file. However, please do not share any data with anyone as they will still be able to decrypt the encrypted password if you have shared the key file as well.
6. If the website design has been changed, you can expect this program to break if it is not maintained/updated.

## FAQ
1. Why didn't you make a fantia_manual_login program?
     * Well... The thing is that I did make the program. However, it was a failure as despite retrieving the login session cookies from fantia, I was still unable to login.
     * Therefore, there is only the pixiv_manual_login program for now.  

## Final Notes
1. Please remember that this was meant to be a mini-project which is meant to be used for personal use.
2. I am still an amateur in programming so if there is a bug, I may or may not be able to fix it. However, I will still do my best of course.
3. If you would like to improve on this program, you can fork this repository and make your own version and make a pull request.
4. Though, I may or may not maintain this program depending on the workload I have as a student.