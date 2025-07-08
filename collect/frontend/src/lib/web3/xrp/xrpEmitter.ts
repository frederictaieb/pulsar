
  
interface XrpPayload {
  latitude: number | null;
  longitude: number | null;
  data: string;
}

export interface XrpResult {
  [key: string]: unknown; // à remplacer par un typage précis si possible
}

export async function xrpEmitter(payload: XrpPayload): Promise<XrpResult> {
    const response = await fetch(`${process.env.NEXT_PUBLIC_FASTAPI_URL}/api/web3/xrp/send_memo`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ payload }),
    });
  
    if (!response.ok) {
      throw new Error("Failed to send XRP transaction");
    }
  
    return response.json();
}
  