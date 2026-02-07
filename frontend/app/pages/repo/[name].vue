<script setup>
const route = useRoute();
const router = useRouter();
const { events } = useEventStream();

const repoName = route.params.name;

const repoEvents = computed(() => {
  return events.value.filter(
    (e) => e.repo_name === decodeURIComponent(repoName),
  );
});

const stats = computed(() => {
  return {
    count: repoEvents.value.length,
    lastActive:
      repoEvents.value.length > 0
        ? new Date(repoEvents.value[0].created_at).toLocaleString()
        : "N/A",
  };
});
</script>

<template>
  <div class="p-8">
    <button
      class="mb-6 flex items-center gap-2 text-slate-400 hover:text-white transition-colors"
      @click="router.back()"
    >
      ← Back to Dashboard
    </button>

    <div class="flex items-center gap-4 mb-8">
      <div
        class="w-16 h-16 rounded-2xl bg-blue-600 flex items-center justify-center text-3xl shadow-lg shadow-blue-900/50"
      >
        📦
      </div>
      <div>
        <h1 class="text-3xl font-bold text-white">
          {{ decodeURIComponent(repoName) }}
        </h1>
        <p class="text-slate-400">Repository History</p>
      </div>
    </div>

    <div class="grid grid-cols-2 gap-4 mb-8 max-w-2xl">
      <div class="p-6 rounded-xl bg-slate-900 border border-slate-800">
        <p class="text-xs text-slate-500 uppercase">Events Captured</p>
        <p class="text-3xl font-mono mt-1">{{ stats.count }}</p>
      </div>
      <div class="p-6 rounded-xl bg-slate-900 border border-slate-800">
        <p class="text-xs text-slate-500 uppercase">Last Activity</p>
        <p class="text-xl font-mono mt-1 text-blue-400">
          {{ stats.lastActive }}
        </p>
      </div>
    </div>

    <h3 class="text-xl font-bold mb-4 text-slate-300">Recent Activity</h3>
    <div class="space-y-3">
      <div
        v-for="event in repoEvents"
        :key="event.id"
        class="p-4 rounded-lg bg-slate-900/50 border border-slate-800 flex items-center gap-4"
      >
        <span class="text-2xl">{{
          event.event_type === "PushEvent" ? "🚀" : "⭐"
        }}</span>
        <div>
          <p class="font-bold text-slate-200">{{ event.actor_name }}</p>
          <p class="text-xs text-slate-500">
            {{ event.event_type }} •
            {{ new Date(event.created_at).toLocaleTimeString() }}
          </p>
        </div>
      </div>

      <div v-if="repoEvents.length === 0" class="text-slate-500 italic py-8">
        No events captured for this repository in the current session.
      </div>
    </div>
  </div>
</template>
