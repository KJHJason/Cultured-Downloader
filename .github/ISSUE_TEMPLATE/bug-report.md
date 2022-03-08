---
name: Bug Report
about: Thanks for taking the time to fill out this bug report!
title: 'Bug Report'
labels: bug
assignees: KJHJason

---
body:
  - type: dropdown
      id: programName
      attributes:
        label: Which program are you seeing this problem on?
        multiple: false
        options:
          - cultured_downloader.exe
          - cultured_downloader.py
          - pixiv_manual_login.exe
          - pixiv_manual_login.py
      validations:
        required: true

    - type: dropdown
      id: browser
      attributes:
        label: Webdriver/Browser Used
        multiple: false
        options:
          - Chrome
          - Edge
      validations:
        required: true

    - type: input
      id: programVersion
      attributes:
        label: Program Version
        description: What version of the program are you using? (Can be found when running the program)

    - type: dropdown
      id: platform
      attributes:
        label: Platform
        multiple: false
        options:
          - Windows
          - Linux
      validations:
        required: true

    - type: textarea
      id: stepsToReproduce
      attributes:
        label: Steps to reproduce the bug
        description: This will assist me in finding where it went wrong.
        placeholder: Please enter the steps to reproduce the bug that you have encountered...
        value: |
               1. 
               2. 
               3. 
               4.
      validations:
        required: true

    - type: textarea
      id: expectedBehaviour
      attributes:
        label: Expected behaviour
        description: A clear and concise description of what you expected to happen.
        placeholder: Explain what should have happened instead...
      validations:
        required: true

    - type: textarea
      id: errorLogText
      attributes:
        label: Relevant log output
        description: If applicable, please copy and paste the text in the error log text files (found in your AppData's LocalLow folder) and paste it here.
        render: shell

    - type: textarea
      id: screenshots
      attributes:
        label: Screenshots
        description: Screenshots can be uploaded by simply dragging an image file into this box
