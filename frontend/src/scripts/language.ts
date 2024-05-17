import { Translate  } from "./wailsjs/go/app/App";
let cachedLang: string = "";

export const EN = "en";
export const JP = "ja";
export const LANGUAGES = [
    { value: EN, name: "English" },
    { value: JP, name: "日本語" },
]

export const translate = (text: string, elId: string, lang: string = ""): void => {
    Translate(text, lang).then((translatedText: string) => {
        const element = document.getElementById(elId);
        if (element) {
            element.textContent = translatedText;
        }
    });
}

export const translateText = (text: string, lang: string = ""): Promise<string> => {
    return Translate(text, lang);
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
