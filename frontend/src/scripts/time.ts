export const convertMinsToMinsAndSecs = (minutes: number): [number, number] => {
    if (minutes < 0) {
        return [0, 0];
    }

    const mins: number = Math.floor(minutes);
    const seconds: number = Math.round((minutes % 1) * 60);
    return [mins, seconds];
}
