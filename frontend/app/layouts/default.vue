<template>
  <div class="flex h-screen bg-slate-950 text-white font-sans overflow-hidden">
    <aside class="w-64 bg-slate-900 border-r border-slate-800 flex flex-col">
      <div class="p-6 border-b border-slate-800">
        <h1
          class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-blue-500"
        >
          GitPulse
        </h1>
      </div>

      <nav class="flex-1 p-4 space-y-2">
        <NuxtLink
          to="/"
          class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all hover:bg-slate-800 text-gray-400 hover:text-white"
          active-class="bg-blue-600/10 text-blue-400 border border-blue-500/20"
        >
          <span>📊</span> Dashboard
        </NuxtLink>

        <NuxtLink
          to="/feed"
          class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all hover:bg-slate-800 text-gray-400 hover:text-white"
          active-class="bg-blue-600/10 text-blue-400 border border-blue-500/20"
        >
          <span>📡</span> Live Feed
        </NuxtLink>
      </nav>

      <div
        class="p-4 border-t border-slate-800 text-xs text-gray-600 text-center"
      >
        v1.0.0 • Connected
      </div>
    </aside>

    <main class="flex-1 overflow-y-auto relative">
      <slot />
    </main>
  </div>
</template>
