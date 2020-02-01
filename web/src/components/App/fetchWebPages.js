// This environment variable is set by webpack when creating the code bundle
const API_SEARCH_URL =
  process.env.REACT_APP_API_URL || "http://localhost:3456/api/v1.0.0/search";

async function fetchWebPages(filter) {
  const response = await fetch(API_SEARCH_URL, {
    headers: { "Content-Type": "application/json" },
    method: "POST",
    body: JSON.stringify({ filter })
  });

  return response.json();
}

export { fetchWebPages };
