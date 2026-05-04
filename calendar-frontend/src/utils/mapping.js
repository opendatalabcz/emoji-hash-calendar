export function buildUserMapping(userMappings) {
    const mapping = {};

    userMappings.forEach(({ keyword, emoji }) => {
        if (keyword && emoji) {
            mapping[keyword.toLowerCase()] = emoji;
        }
    });

    return mapping;
}