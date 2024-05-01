import { GetLanguage } from "./wailsjs/go/app/App";

let cachedLang: string = "";
const EN = "en";
const JP = "ja";
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
}

export const InitialiseLanguage = async (): Promise<void> => {
    cachedLang = await GetLanguage();
    console.log("Language initialised to", cachedLang);
}

export const Translate = (text: string): string => {
    if (cachedLang === "") {
        throw new Error("Language not initialised");
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
