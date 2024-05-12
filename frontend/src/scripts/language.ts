let cachedLang: string = "";

export const EN = "en";
export const JP = "ja";
export const LANGUAGES = [
    { value: EN, name: "English" },
    { value: JP, name: "日本語" },
]

const textMap: Record<string, Record<string, string>> = {
    "hello": {
		[EN]: "Hello",
		[JP]: "こんにちは",
	},
	"date/time": {
		[EN]: "Date/Time",
		[JP]: "日時",
	},
	"your input": {
		[EN]: "Your Inputs",
		[JP]: "あなたの入力",
	},
    "inputs": {
        [EN]: "Inputs",
        [JP]: "入力",
    },
	"progress": {
		[EN]: "Progress",
		[JP]: "進捗",
	},
	"actions": {
		[EN]: "Actions",
		[JP]: "アクション",
	},
    "current task": {
        [EN]: "Current Task",
        [JP]: "現在のタスク",
    },
    "save": {
        [EN]: "Save",
        [JP]: "保存",
    },
    "unknown": {
        [EN]: "Unknown",
        [JP]: "不明",
    },
    "welcome to cultured downloader!": {
        [EN]: "Welcome to Cultured Downloader!",
        [JP]: "Cultured Downloaderへようこそ！",
    },
    "home": {
        [EN]: "Home",
        [JP]: "ホーム",
    },
    "downloads": {
        [EN]: "Downloads",
        [JP]: "ダウンロード",
    },
    "settings": {
        [EN]: "Settings",
        [JP]: "設定",
    },
    "light mode": {
        [EN]: "Light Mode",
        [JP]: "ライトモード",
    },
    "dark mode": {
        [EN]: "Dark Mode",
        [JP]: "ダークモード",
    },
}
export const Translate = (text: string, language: string = cachedLang): string => {
    if (language === "") {
        throw new Error("language is empty or has not been initialised!")
    }

    const textKey = text.toLowerCase().trim();
    if (textMap[textKey] === undefined) {
        return text;
    }
    return textMap[textKey][cachedLang] ?? text;
}

export const GetLocale = (): string => {
    switch (cachedLang) {
        case JP:
            return "ja-JP";
        default:
            return "en-US";
    }
}

export const GetCachedLanguage = (): string => {
    return cachedLang;
}

export const ChangeCachedLanguage = (lang: string): void => {
    cachedLang = lang;
}
