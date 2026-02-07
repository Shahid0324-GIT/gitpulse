export interface GithubEvent {
  id: string;
  repo_name: string;
  event_type: string;
  actor_name: string;
  created_at: string;
}

export const useEventStream = () => {
  const events = useState<GithubEvent[]>("events", () => []);
  const isConnected = useState<boolean>("isConnected", () => false);
  const eventCount = useState<number>("eventCount", () => 0);

  let ws: WebSocket | null = null;

  const connect = () => {
    if (import.meta.server) return;
    if (isConnected.value) return;

    const config = useRuntimeConfig();

    ws = new WebSocket(config.public.wsBase as string);

    ws.onopen = () => {
      console.log("✅ WS Connected!");
      isConnected.value = true;
    };

    ws.onmessage = (msg: MessageEvent) => {
      try {
        const newEvent: GithubEvent = JSON.parse(msg.data);

        events.value.unshift(newEvent);

        if (events.value.length > 500) {
          events.value.pop();
        }

        eventCount.value++;
      } catch (e) {
        console.error("Failed to parse WebSocket message:", e);
      }
    };

    ws.onclose = () => {
      console.log("❌ WS Disconnected");
      isConnected.value = false;
      ws = null;

      // Auto-Reconnect Logic: Try again in 3 seconds
      setTimeout(() => connect(), 3000);
    };

    ws.onerror = (error: Event) => {
      console.error("WebSocket Error:", error);
      ws?.close();
    };
  };

  // 5. DISCONNECT FUNCTION (Cleanup)
  const disconnect = () => {
    if (ws) {
      ws.close();
      ws = null;
      isConnected.value = false;
    }
  };

  return {
    events,
    isConnected,
    eventCount,
    connect,
    disconnect,
  };
};
