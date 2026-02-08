<script setup>
const route = useRoute();
const { events } = useEventStream();

const repoName = decodeURIComponent(route.params.name);

const ownerName = computed(() => repoName.split("/")[0] || "github");

const repoEvents = computed(() => {
  return events.value.filter((e) => e.repo_name === repoName);
});

const stats = computed(() => {
  const count = repoEvents.value.length;
  const lastEvent = repoEvents.value[0];

  return {
    count,
    lastActive:
      count > 0
        ? new Date(lastEvent.created_at).toLocaleString()
        : "Waiting for data...",
    contributors: new Set(repoEvents.value.map((e) => e.actor_name)).size,
  };
});

const getEventIcon = (type) => {
  if (type === "PushEvent") return "🚀";
  if (type === "WatchEvent") return "⭐";
  if (type === "PullRequestEvent") return "🔀";
  if (type === "IssuesEvent") return "🐛";
  return "📦";
};
</script>

<template>
  <div
    class="min-h-screen bg-[#0d1117] bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-[#0d1117] to-black p-6 sm:p-12 pb-32"
  >
    <NuxtLink
      to="/"
      class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[#161b22] border border-[#30363d] text-slate-400 hover:text-white hover:border-slate-500 transition-all mb-8 group"
    >
      <span class="group-hover:-translate-x-1 transition-transform">←</span>
      Back to Command Center
    </NuxtLink>

    <div
      class="relative group overflow-hidden rounded-3xl p-[1px] bg-gradient-to-b from-blue-500/20 to-transparent mb-8"
    >
      <div
        class="bg-[#161b22]/80 backdrop-blur-xl p-8 rounded-3xl flex flex-col md:flex-row items-center md:items-start gap-6 relative z-10"
      >
        <img
          :src="`https://github.com/${ownerName}.png`"
          alt="Owner Avatar"
          class="w-20 h-20 md:w-24 md:h-24 rounded-2xl border-2 border-[#30363d] shadow-2xl bg-black"
        />

        <div class="text-center md:text-left flex-1">
          <h1
            class="text-3xl md:text-5xl font-black text-white tracking-tight mb-2 break-all"
          >
            {{ repoName }}
          </h1>
          <div class="flex flex-wrap justify-center md:justify-start gap-3">
            <a
              :href="`https://github.com/${repoName}`"
              target="_blank"
              class="px-4 py-1.5 rounded-full bg-[#238636] text-white text-sm font-bold hover:bg-[#2ea043] transition-colors flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path
                  d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
                />
              </svg>
              View on GitHub
            </a>
            <span
              class="px-3 py-1.5 rounded-full border border-[#30363d] text-slate-400 text-xs font-mono flex items-center gap-2"
            >
              <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              Tracking Live
            </span>
          </div>
        </div>
      </div>
      <div class="absolute inset-0 bg-blue-500/5 pointer-events-none" />
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-12">
      <div class="p-6 rounded-2xl bg-[#161b22] border border-[#30363d]">
        <p class="text-xs text-slate-500 uppercase font-bold tracking-wider">
          Session Events
        </p>
        <p class="text-3xl font-mono mt-2 text-white">{{ stats.count }}</p>
      </div>
      <div class="p-6 rounded-2xl bg-[#161b22] border border-[#30363d]">
        <p class="text-xs text-slate-500 uppercase font-bold tracking-wider">
          Active Users
        </p>
        <p class="text-3xl font-mono mt-2 text-blue-400">
          {{ stats.contributors }}
        </p>
      </div>
      <div class="p-6 rounded-2xl bg-[#161b22] border border-[#30363d]">
        <p class="text-xs text-slate-500 uppercase font-bold tracking-wider">
          Last Signal
        </p>
        <p class="text-sm font-mono mt-3 text-emerald-400 truncate">
          {{ stats.lastActive }}
        </p>
      </div>
    </div>

    <h3 class="text-xl font-bold mb-6 text-white flex items-center gap-2">
      <span class="w-1 h-6 bg-blue-500 rounded-full" />
      Live Transmission Log
    </h3>

    <div class="space-y-3">
      <TransitionGroup name="list">
        <div
          v-for="event in repoEvents"
          :key="event.id"
          class="p-4 rounded-xl bg-[#161b22]/50 border border-[#30363d] hover:border-blue-500/30 transition-all flex items-center gap-4 group relative overflow-hidden"
          :class="{ 'border-red-900/30 bg-red-900/5': event.is_bot }"
        >
          <a
            :href="`https://github.com/${event.actor_name}`"
            target="_blank"
            class="shrink-0 relative"
          >
            <img
              :src="
                event.is_bot
                  ? 'https://github.githubassets.com/images/mona-whisper.gif'
                  : `https://github.com/${event.actor_name}.png`
              "
              class="w-10 h-10 rounded-full border border-slate-700 bg-black group-hover:scale-110 transition-transform"
            />
            <div
              class="absolute -bottom-1 -right-1 w-5 h-5 rounded-full bg-[#161b22] border border-[#30363d] flex items-center justify-center text-[10px]"
            >
              {{ getEventIcon(event.event_type) }}
            </div>
          </a>

          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-0.5">
              <a
                :href="`https://github.com/${event.actor_name}`"
                target="_blank"
                class="font-bold text-slate-200 hover:text-blue-400 hover:underline truncate"
              >
                {{ event.actor_name }}
              </a>
              <span
                v-if="event.is_bot"
                class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-red-500/10 text-red-400 border border-red-500/20 uppercase"
                >BOT</span
              >
            </div>
            <p class="text-xs text-slate-500 flex items-center gap-2">
              <span class="text-slate-400">{{ event.event_type }}</span>
              <span>•</span>
              <span class="font-mono">{{
                new Date(event.created_at).toLocaleTimeString()
              }}</span>
            </p>
          </div>

          <a
            :href="`https://github.com/${repoName}`"
            target="_blank"
            class="text-xs px-3 py-1.5 rounded-lg bg-[#0d1117] border border-[#30363d] text-slate-400 hover:text-white hover:border-slate-500 transition-colors opacity-0 group-hover:opacity-100"
          >
            View →
          </a>
        </div>
      </TransitionGroup>

      <div
        v-if="repoEvents.length === 0"
        class="text-center py-12 rounded-xl border border-dashed border-[#30363d]"
      >
        <p class="text-4xl mb-4 grayscale opacity-20">📡</p>
        <p class="text-slate-500 italic">
          No signals detected in current session.
        </p>
        <p class="text-xs text-slate-600 mt-2">
          Waiting for live transmission...
        </p>
      </div>
    </div>
  </div>
</template>
