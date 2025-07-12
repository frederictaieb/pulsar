export interface XrpTransactionMessage {
  type: string;
  transaction: {
    Memos: Array<{
      Memo: {
        MemoData: string;
      };
    }>;
    [key: string]: unknown;
  };
  [key: string]: unknown;
}

export function createXrpWebSocket(
  url: string,
  walletAddress: string,
  onMessage: (data: XrpTransactionMessage) => void,
  onError?: (err: Event | ErrorEvent) => void,
  onClose?: () => void
) {
  const ws = new WebSocket(url);

  ws.onopen = () => {
    console.log("WebSocket opened");
    ws.send(
      JSON.stringify({
        id: 1,
        command: "subscribe",
        accounts: [walletAddress],
      })
    );
  };

  ws.onmessage = (event) => {
    const data: unknown = JSON.parse(event.data);
    console.log("data received :", data);
    onMessage(data as XrpTransactionMessage);
  };

  ws.onerror = onError || ((err: Event | ErrorEvent) => console.error("WebSocket error:", err));
  ws.onclose = onClose || (() => console.log("WebSocket closed"));

  return ws;
}
