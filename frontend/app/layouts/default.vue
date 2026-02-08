<script setup>
const { countdown } = useEventStream();
</script>

<template>
  <div
    class="min-h-screen bg-[#0d1117] text-slate-300 font-sans selection:bg-[#2ea043] selection:text-white pb-24"
  >
    <main class="max-w-7xl mx-auto w-full">
      <slot />
    </main>

    <nav class="fixed bottom-6 left-1/2 -translate-x-1/2 z-50">
      <div
        class="flex items-center gap-1 p-2 rounded-full bg-[#161b22]/90 backdrop-blur-md border border-slate-800 shadow-2xl ring-1 ring-white/10"
      >
        <NuxtLink
          to="/"
          active-class="bg-[#2ea043] text-white shadow-lg shadow-green-900/50"
          class="p-3 rounded-full transition-all hover:bg-white/10"
          title="Dashboard"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect width="7" height="9" x="3" y="3" rx="1" />
            <rect width="7" height="5" x="14" y="3" rx="1" />
            <rect width="7" height="9" x="14" y="12" rx="1" />
            <rect width="7" height="5" x="3" y="16" rx="1" />
          </svg>
        </NuxtLink>

        <NuxtLink
          to="/feed"
          active-class="bg-[#2ea043] text-white shadow-lg shadow-green-900/50"
          class="p-3 rounded-full transition-all hover:bg-white/10"
          title="Live Feed"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M4.9 19.1C1 15.2 1 8.8 4.9 4.9" />
            <path d="M7.8 16.2c-2.3-2.3-2.3-6.1 0-8.5" />
            <circle cx="12" cy="12" r="2" />
          </svg>
        </NuxtLink>

        <div class="w-px h-6 bg-slate-700 mx-1" />

        <div
          class="px-3 flex items-center gap-2 text-xs font-mono text-[#2ea043] min-w-[100px] justify-center"
        >
          <span class="relative flex h-2 w-2">
            <span
              v-if="countdown > 0"
              class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"
            />
            <span
              class="relative inline-flex rounded-full h-2 w-2"
              :class="countdown === 0 ? 'bg-amber-500' : 'bg-green-500'"
            />
          </span>

          <span v-if="countdown > 0">NEXT: {{ countdown }}s</span>
          <span v-else class="text-amber-500 animate-pulse">SYNCING...</span>
        </div>
      </div>
    </nav>
  </div>
</template>
