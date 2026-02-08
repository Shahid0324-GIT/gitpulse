export interface GithubEvent {
  id: string;
  repo_name: string;
  event_type: string;
  actor_name: string;
  created_at: string;
  is_bot?: boolean;
  language?: string;
}

let ws: WebSocket | null = null;
let timerInterval: NodeJS.Timeout | null = null;

export const useEventStream = () => {
  const events = useState<GithubEvent[]>("events", () => []);
  const isConnected = useState<boolean>("isConnected", () => false);
  const eventCount = useState<number>("eventCount", () => 0);
  const countdown = useState<number>("countdown", () => 60);

  const startTimer = () => {
    if (timerInterval) clearInterval(timerInterval);

    countdown.value = 60;

    timerInterval = setInterval(() => {
      if (countdown.value > 0) {
        countdown.value--;
      }
    }, 1000);
  };

  const connect = async () => {
    if (import.meta.server) return;
    if (isConnected.value) return;

    const config = useRuntimeConfig();

    try {
      const res = await fetch(`${config.public.apiBase}/stats/total`);
      if (res.ok) {
        const data = await res.json();
        eventCount.value = data.count;
      }
    } catch (e) {
      console.error(e);
    }

    ws = new WebSocket(config.public.wsBase as string);

    ws.onopen = () => {
      console.log("✅ WS Connected");
      isConnected.value = true;
      startTimer();
    };

    ws.onmessage = (msg: MessageEvent) => {
      try {
        const rawData = JSON.parse(msg.data);
        if (!rawData.id) return;

        events.value.unshift(rawData);
        if (events.value.length > 500) events.value.pop();
        eventCount.value++;

        if (countdown.value < 55) {
          countdown.value = 60;
        }
      } catch (e) {
        console.error(e);
      }
    };

    ws.onclose = () => {
      isConnected.value = false;
      ws = null;
      if (timerInterval) clearInterval(timerInterval);
      setTimeout(() => connect(), 3000);
    };
  };

  return {
    events,
    isConnected,
    eventCount,
    countdown,
    connect,
  };
};
