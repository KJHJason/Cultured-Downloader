import { Translate  } from "./wailsjs/go/app/App";
let cachedLang: string = "";

export const EN = "en";
export const JP = "ja";
export const LANGUAGES = [
    { value: EN, name: "English" },
    { value: JP, name: "日本語" },
]

export const translateText = (text: string, lang: string = "", fallback: string = ""): Promise<string> => {
    return Translate(text, fallback, lang);
}

export const translate = (text: string, elId: string, lang: string = "", fallback: string = ""): void => {
    translateText(text, lang, fallback).then((translatedText: string) => {
        const element = document.getElementById(elId);
        if (element) {
            element.textContent = translatedText;
        }
    });
}

export const translateEl = async (text: string, el: HTMLElement, lang: string = "", fallback: string = ""): Promise<void> => {
    if (!el) 
        throw new Error("Element is null");
    el.textContent = await translateText(text, lang, fallback);
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
