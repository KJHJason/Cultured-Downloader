const titleCase = (s: string): string => {
    return s.toLowerCase().replace(/(^|\s)\S/g, (c: string) => {
        return c.toUpperCase(); // replace first letter of each word with uppercase
    });
}

const actionTitleCase = (s: string): string => {
    return titleCase(
        s.replace(/_/g, " ") // replace underscores with spaces
    );
};

export { titleCase, actionTitleCase };
