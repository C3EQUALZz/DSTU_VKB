function truncateText(text, maxLength) {
  if (!text) return "";
  if (text.length <= maxLength) {
    return text;
  } else if (text.indexOf("/") !== -1) {
    const ellipsis = "...";
    const parts = text.split("/");
    const firstPart = parts[0];
    const lastPart = parts[parts.length - 1];
    const middleParts = parts.slice(1, parts.length - 1);
    let truncatedText = firstPart + "/";
    for (let i = 0; i < middleParts.length; i++) {
      if (
        truncatedText.length + middleParts[i].length + ellipsis.length >
        maxLength
      ) {
        truncatedText += ellipsis;
        break;
      }
      truncatedText += middleParts[i] + "/";
    }
    truncatedText += "/" + lastPart;
    return truncatedText;
  } else {
    const ellipsis = "...";
    const truncatedText = text.slice(0, maxLength - ellipsis.length) + ellipsis;
    return truncatedText;
  }
}

function extractOrderByClause(queryFilter) {
  const orderByRegex = /\bORDER\s+BY\s+([\w\s",.]+)$/i;
  const match = queryFilter.match(orderByRegex);

  if (!match) return { queryFilterCleaned: queryFilter, orderByClause: "" };

  const queryFilterCleaned = queryFilter.replace(orderByRegex, "").trim();
  return { queryFilterCleaned, orderByClause: `ORDER BY ${match[1]}` };
}

export { truncateText, extractOrderByClause };
