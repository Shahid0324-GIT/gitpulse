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
        class="p-4 rounded-xl bg-gradient-to-r from-[#161b22] to-[#0d1117] border border-[#30363d] hover:border-green-500/30 transition-all duration-300 flex items-center gap-4 group relative overflow-hidden shadow-lg hover:shadow-green-900/10 hover:-translate-y-0.5"
        :class="{
          'border-red-900/30 from-red-900/10 to-[#0d1117]': event.is_bot,
        }"
      >
        <div class="relative shrink-0">
          <img
            :src="
              event.is_bot
                ? 'https://github.githubassets.com/images/mona-whisper.gif'
                : `https://github.com/${event.actor_name}.png`
            "
            class="w-12 h-12 rounded-full border border-slate-700 bg-slate-800"
            loading="lazy"
            alt="User Avatar"
          />

          <div
            class="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-slate-800 border border-slate-900 flex items-center justify-center text-xs shadow-sm"
          >
            <span v-if="event.event_type === 'PushEvent'">🚀</span>
            <span v-else-if="event.event_type === 'WatchEvent'">⭐</span>
            <span v-else-if="event.event_type === 'CreateEvent'">✨</span>
            <span v-else-if="event.event_type === 'IssuesEvent'">🐛</span>
            <span v-else-if="event.event_type === 'PullRequestEvent'">🔀</span>
            <span v-else>📦</span>
          </div>
        </div>

        <div class="flex-1 min-w-0 z-10">
          <NuxtLink
            :to="`/repo/${encodeURIComponent(event.repo_name)}`"
            class="text-blue-400 font-bold group-hover:text-blue-300 hover:underline block truncate text-lg"
          >
            {{ event.repo_name }}
          </NuxtLink>

          <div class="flex items-center gap-2 text-xs text-slate-500 truncate">
            <span class="text-slate-300 font-medium">{{
              event.actor_name
            }}</span>

            <span
              v-if="event.is_bot"
              class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-red-500/10 text-red-400 border border-red-500/20 uppercase tracking-wider"
            >
              BOT
            </span>

            <span>•</span>
            <span>{{ new Date(event.created_at).toLocaleTimeString() }}</span>
          </div>
        </div>

        <span
          class="text-xs px-2 py-1 rounded bg-slate-800 text-slate-400 shrink-0 hidden sm:inline-block border border-slate-700"
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
