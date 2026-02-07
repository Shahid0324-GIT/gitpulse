<script setup>
useHead({ title: "Dashboard" });

const { events, eventCount, isConnected, connect } = useEventStream();

const config = useRuntimeConfig();

onMounted(async () => {
  connect();

  try {
    const response = await fetch(`${config.public.apiBase}/events/?limit=500`);
    if (response.ok) {
      const initialData = await response.json();
      events.value = initialData;
      eventCount.value = initialData.length;
    }
  } catch (e) {
    console.error("Failed to fetch initial history:", e);
  }
});
</script>

<template>
  <div class="p-8 space-y-8">
    <div class="flex justify-between items-end">
      <div>
        <h2 class="text-3xl font-bold text-white">Dashboard</h2>
        <p class="text-slate-400">Real-time metrics from the global grid</p>
      </div>
      <div
        :class="
          isConnected
            ? 'bg-green-500/20 text-green-400'
            : 'bg-red-500/20 text-red-400'
        "
        class="px-3 py-1 rounded-full text-xs font-mono border border-current transition-colors"
      >
        {{ isConnected ? "● LIVE STREAM" : "○ DISCONNECTED" }}
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div
        class="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 backdrop-blur-sm"
      >
        <p class="text-sm text-slate-500 uppercase tracking-wider">
          Total Events Received
        </p>
        <p class="text-4xl font-mono mt-2 text-white">{{ eventCount }}</p>
      </div>

      <div
        class="p-6 rounded-2xl bg-slate-900/50 border border-slate-800 backdrop-blur-sm col-span-2"
      >
        <p class="text-sm text-slate-500 uppercase tracking-wider">
          Latest Action
        </p>
        <div v-if="events.length > 0" class="mt-2 flex items-center gap-3">
          <span class="text-2xl">🚀</span>
          <div>
            <p class="text-xl font-bold text-teal-400">
              {{ events[0].repo_name }}
            </p>
            <p class="text-sm text-slate-400">by {{ events[0].actor_name }}</p>
          </div>
        </div>
        <p v-else class="mt-2 text-xl text-slate-600">Waiting for data...</p>
      </div>
    </div>

    <div class="h-96 rounded-2xl bg-slate-900/50 border border-slate-800 p-6">
      <h3 class="text-lg font-bold text-slate-300 mb-4">Event Distribution</h3>
      <ActivityChart :events="events" />
    </div>
  </div>
</template>
