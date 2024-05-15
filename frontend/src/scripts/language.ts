let cachedLang: string = "";

export const EN = "en";
export const JP = "ja";
export const LANGUAGES = [
    { value: EN, name: "English" },
    { value: JP, name: "日本語" },
]

const textMap: Record<string, Record<string, string>> = {
    // Download queue
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
    "downloads": {
        [EN]: "Downloads",
        [JP]: "ダウンロード",
    },
    // General
    "save": {
        [EN]: "Save",
        [JP]: "保存",
    },
    "unknown": {
        [EN]: "Unknown",
        [JP]: "不明",
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
    // Home Page
    "to get started, click on one of the options below or use the navigation bar in the top-left corner.": {
        [EN]: "To get started, click on one of the options below or use the navigation bar in the top-left corner.",
        [JP]: "始めるには、以下のオプションのいずれかをクリックするか、左上隅のナビゲーションバーを使用してください。",
    },
    "welcome back,": {
        [EN]: "Welcome back,",
        [JP]: "おかえりなさい、",
    },
    "!": {
        [EN]: "!",
        [JP]: "！",
    },
    "home": {
        [EN]: "Home",
        [JP]: "ホーム",
    },
    "image:": {
        [EN]: "Image:",
        [JP]: "イラスト：",
    },
    "karutamo": {
        [EN]: "Karutamo",
        [JP]: "かるたも",
    },
    "found an issue? click me!": {
        [EN]: "Found an issue? Click me!",
        [JP]: "問題を発見しましたか？私をクリックしてください！",
    },
    // Program info
    "check for updates": {
        [EN]: "Check for Updates",
        [JP]: "更新を確認",
    },
    "checking for updates...": {
        [EN]: "Checking for updates...",
        [JP]: "更新を確認中...",
    },
    "outdated, last checked at": {
        [EN]: "Outdated, last checked at ",
        [JP]: "古い、最後に確認した日時",
    },
    "up-to-date, last checked at" : {
        [EN]: "Up-to-date, last checked at ",
        [JP]: "最新、最後に確認した日時",
    },
    // pagination
    "previous": {
        [EN]: "Previous",
        [JP]: "前",
    },
    "next": {
        [EN]: "Next",
        [JP]: "次",
    },
    "showing": {
        [EN]: "Showing",
        [JP]: "エントリーの表示:",
    },
    "to": {
        [EN]: "to",
        [JP]: "から",
    },
    "of": {
        [EN]: "of",
        [JP]: "までの",
    },
    "entries": {
        [EN]: "Entries",
        [JP]: "エントリー",
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
    return textMap[textKey][language] ?? text;
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
