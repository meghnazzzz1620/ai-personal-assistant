const BASE_URL = "http://localhost:8000";

export const sendMessageStream = async (message, token, onChunk) => {
  const response = await fetch(
    `${BASE_URL}/chat?message=${encodeURIComponent(message)}`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  );

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    onChunk(chunk);
  }
};
