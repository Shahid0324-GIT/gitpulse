<script setup>
useHead({ title: "Live Feed" });
const { events, connect } = useEventStream();
const config = useRuntimeConfig();

const isLoadingMore = ref(false);
const hasMore = ref(true);

async function loadMore() {
  if (isLoadingMore.value || !hasMore.value) return;

  isLoadingMore.value = true;

  try {
    const currentOffset = events.value.length;

    const response = await fetch(
      `${config.public.apiBase}/events/?limit=50&offset=${currentOffset}`,
    );

    if (!response.ok) throw new Error("API Error");

    const newEvents = await response.json();

    if (newEvents.length > 0) {
      events.value.push(...newEvents);
    }

    if (newEvents.length < 50) {
      hasMore.value = false;
    }
  } catch (e) {
    console.error("Pagination error:", e);
  } finally {
    isLoadingMore.value = false;
  }
}

onMounted(() => {
  connect();
  if (events.value.length === 0) {
    loadMore();
  }
});
</script>

<template>
  <div class="p-8">
    <h2 class="text-2xl font-bold mb-6 text-white">Live Event Stream</h2>

    <TransitionGroup name="list" tag="div" class="space-y-3">
      <div
        v-for="event in events"
        :key="event.id"
        class="p-4 rounded-xl bg-slate-900 border border-slate-800 hover:border-blue-500/30 transition-all flex items-center gap-4 group"
      >
        <div
          class="w-10 h-10 rounded-full bg-slate-800 group-hover:bg-blue-900/30 flex items-center justify-center transition-colors shrink-0"
        >
          <span v-if="event.event_type === 'PushEvent'">🚀</span>
          <span v-else-if="event.event_type === 'WatchEvent'">⭐</span>
          <span v-else-if="event.event_type === 'CreateEvent'">✨</span>
          <span v-else-if="event.event_type === 'IssuesEvent'">🐛</span>
          <span v-else-if="event.event_type === 'PullRequestEvent'">🔀</span>
          <span v-else>📦</span>
        </div>

        <div class="flex-1 min-w-0">
          <NuxtLink
            :to="`/repo/${encodeURIComponent(event.repo_name)}`"
            class="text-blue-400 font-bold group-hover:text-blue-300 hover:underline block truncate"
          >
            {{ event.repo_name }}
          </NuxtLink>
          <p class="text-xs text-slate-500 truncate">
            <span class="text-slate-300">{{ event.actor_name }}</span> •
            {{ new Date(event.created_at).toLocaleTimeString() }}
          </p>
        </div>

        <span
          class="text-xs px-2 py-1 rounded bg-slate-800 text-slate-400 shrink-0 hidden sm:inline-block"
        >
          {{ event.event_type }}
        </span>
      </div>
    </TransitionGroup>
    <div class="mt-8 text-center py-4">
      <button
        v-if="hasMore"
        :disabled="isLoadingMore"
        class="px-8 py-3 rounded-full bg-slate-800 border border-slate-700 hover:bg-blue-600 hover:border-blue-500 hover:text-white text-slate-300 font-bold transition-all flex items-center gap-2 mx-auto disabled:opacity-50 disabled:cursor-not-allowed"
        @click="loadMore"
      >
        <span v-if="isLoadingMore" class="animate-spin text-xl">⏳</span>
        <span>{{ isLoadingMore ? "Loading..." : "Load Older Events" }}</span>
      </button>

      <p v-else class="text-slate-500 italic">
        You have reached the end of the archives.
      </p>
    </div>
  </div>
</template>

<style scoped>
/* CSS Animation for new items */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
</style>
