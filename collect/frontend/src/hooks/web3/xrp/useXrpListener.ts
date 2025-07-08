// hooks/useXrpListener.ts
import { useEffect, useState } from "react";
import { createXrpWebSocket } from "@/lib/web3/xrp/XrpSocket";

export default function useXrpListener(walletAddress: string | undefined) {
  const [messageContent, setMessageContent] = useState<string>("");

  useEffect(() => {
    if (!walletAddress) return;

    const ws = createXrpWebSocket(
      process.env.NEXT_PUBLIC_TESTNET_URL || "",
      walletAddress,
      (data) => {
        if (data.type === "transaction") {
          const msg = Buffer.from(data.transaction.Memos[0].Memo.MemoData, 'hex').toString('utf-8') || "No Memo";
          setMessageContent(msg);
        }
      }
    );

    return () => ws.close();
  }, [walletAddress]);

  return messageContent;
}
