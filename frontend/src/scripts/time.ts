import { GetLocale } from "./language";

export const convertMinsToMinsAndSecs = (minutes: number): [number, number] => {
    if (minutes < 0) {
        return [0, 0];
    }

    const mins: number = Math.floor(minutes);
    const seconds: number = Math.round((minutes % 1) * 60);
    return [mins, seconds];
}

export const makeDateTimeReadable = (dateTime: string, addSeconds: boolean = false): string => {
    const date = new Date(dateTime);
    const options: Intl.DateTimeFormatOptions = {
        month: "short", day: "numeric", 
        hour: "numeric", minute: "numeric",
    };

    if (addSeconds) {
        options.second = "numeric";
    }
    return date.toLocaleString(GetLocale(), options);
};
