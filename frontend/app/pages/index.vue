<script setup>
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
);

useHead({ title: "Dashboard" });

const { eventCount, isConnected, connect, countdown } = useEventStream();
const config = useRuntimeConfig();

const hourlyData = ref({});
const loadingHeatmap = ref(true);

const showFloating = ref(false);
const floatingDiff = ref(0);
let previousCount = 0;
let debounceTimer = null;

watch(eventCount, (newVal) => {
  if (previousCount === 0) {
    previousCount = newVal;
    return;
  }

  const diff = newVal - previousCount;

  const currentHour = new Date().getUTCHours();

  if (hourlyData.value[currentHour] !== undefined) {
    hourlyData.value[currentHour] += diff;
  } else {
    hourlyData.value[currentHour] = diff;
  }

  if (showFloating.value) {
    floatingDiff.value += diff;
  } else {
    floatingDiff.value = diff;
  }

  previousCount = newVal;

  showFloating.value = true;
  if (debounceTimer) clearTimeout(debounceTimer);

  debounceTimer = setTimeout(() => {
    showFloating.value = false;
    setTimeout(() => {
      floatingDiff.value = 0;
    }, 500);
  }, 4000);
});

onMounted(async () => {
  connect();
  previousCount = eventCount.value;

  try {
    const res = await fetch(`${config.public.apiBase}/stats/hourly`);
    if (res.ok) hourlyData.value = await res.json();
  } catch (e) {
    console.error(e);
  } finally {
    loadingHeatmap.value = false;
  }
});

// --- CHART CONFIG ---
const chartData = computed(() => {
  const hours = Array.from({ length: 24 }, (_, i) => i);
  return {
    labels: hours.map((h) => `${h}:00`),
    datasets: [
      {
        label: "Events",
        data: hours.map((h) => hourlyData.value[h] || 0),
        borderColor: "#2ea043",
        backgroundColor: (context) => {
          const ctx = context.chart.ctx;
          const gradient = ctx.createLinearGradient(0, 0, 0, 400);
          gradient.addColorStop(0, "rgba(46, 160, 67, 0.5)");
          gradient.addColorStop(1, "rgba(46, 160, 67, 0)");
          return gradient;
        },
        fill: true,
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 6,
        borderWidth: 2,
      },
    ],
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: {
      grid: { display: false },
      ticks: { color: "#6e7681", maxRotation: 0, autoSkip: true },
    },
    y: {
      grid: { color: "#30363d" },
      ticks: { color: "#6e7681" },
      beginAtZero: true,
    },
  },
  interaction: {
    mode: "index",
    intersect: false,
  },
};
</script>

<template>
  <div
    class="min-h-screen bg-[#0d1117] bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-[#0d1117] to-black p-6 sm:p-12 space-y-8"
  >
    <header class="text-center space-y-4 mb-16 relative z-10">
      <h1
        class="text-5xl md:text-7xl font-black tracking-tighter text-white drop-shadow-2xl"
      >
        GIT<span
          class="text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-emerald-600"
          >PULSE</span
        >
      </h1>
      <p class="text-slate-400 text-lg font-light tracking-wide">
        Global Open Source Intelligence
      </p>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div
        class="relative group overflow-hidden rounded-2xl p-[1px] bg-gradient-to-b from-white/10 to-transparent"
      >
        <div
          class="bg-[#161b22]/80 backdrop-blur-xl h-full p-6 rounded-2xl flex items-center justify-between"
        >
          <div>
            <p
              class="text-sm text-slate-400 font-medium uppercase tracking-wider"
            >
              System Status
            </p>
            <div class="mt-2 flex items-center gap-3">
              <span class="text-2xl font-bold text-white">
                {{ isConnected ? "Operational" : "Offline" }}
              </span>
              <span class="relative flex h-3 w-3">
                <span
                  v-if="isConnected"
                  class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"
                />
                <span
                  class="relative inline-flex rounded-full h-3 w-3"
                  :class="isConnected ? 'bg-green-500' : 'bg-red-500'"
                />
              </span>
            </div>
          </div>
          <div
            class="text-4xl opacity-20 grayscale group-hover:grayscale-0 transition-all"
          >
            📡
          </div>
        </div>
      </div>

      <div
        class="relative group overflow-hidden rounded-2xl p-[1px] bg-gradient-to-b from-green-500/20 to-transparent"
      >
        <div
          class="bg-[#161b22]/80 backdrop-blur-xl h-full p-6 rounded-2xl relative"
        >
          <p
            class="text-sm text-green-400/80 font-medium uppercase tracking-wider"
          >
            Events Captured
          </p>
          <div class="flex items-baseline gap-2">
            <p
              class="mt-2 text-4xl font-mono font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-slate-400"
            >
              {{ eventCount.toLocaleString() }}
            </p>

            <Transition
              enter-active-class="transition duration-500 ease-out"
              enter-from-class="transform translate-y-4 opacity-0 scale-50"
              enter-to-class="transform translate-y-0 opacity-100 scale-100"
              leave-active-class="transition duration-[2000ms] ease-out"
              leave-from-class="transform translate-y-0 opacity-100"
              leave-to-class="transform -translate-y-12 opacity-0"
            >
              <span
                v-if="showFloating && floatingDiff > 0"
                class="absolute top-4 right-6 text-xl font-bold text-green-400 drop-shadow-lg"
              >
                +{{ floatingDiff }} ⬆
              </span>
            </Transition>
          </div>
        </div>
        <div
          class="absolute inset-0 bg-green-500/5 group-hover:bg-green-500/10 transition-colors pointer-events-none"
        />
      </div>

      <div
        class="relative group overflow-hidden rounded-2xl p-[1px] bg-gradient-to-b from-blue-500/20 to-transparent"
      >
        <div class="bg-[#161b22]/80 backdrop-blur-xl h-full p-6 rounded-2xl">
          <p
            class="text-sm text-blue-400/80 font-medium uppercase tracking-wider"
          >
            Next Data Batch
          </p>
          <p class="mt-2 text-3xl font-bold text-white flex items-center gap-3">
            {{ countdown }}s
            <span class="text-sm font-normal text-slate-500 self-end mb-1"
              >until sync</span
            >
          </p>
        </div>
      </div>
    </div>

    <div
      class="relative rounded-3xl p-[1px] bg-gradient-to-b from-white/10 to-transparent shadow-2xl"
    >
      <div
        class="bg-[#161b22]/60 backdrop-blur-md p-8 rounded-3xl h-[450px] relative"
      >
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-bold text-white flex items-center gap-2">
            <span class="w-2 h-6 bg-green-500 rounded-full" />
            24-Hour Trend
          </h3>
          <span
            class="text-xs text-slate-500 border border-slate-700 px-2 py-1 rounded-full"
            >UTC Time</span
          >
        </div>

        <div
          v-if="loadingHeatmap"
          class="absolute inset-0 flex items-center justify-center text-slate-500 animate-pulse"
        >
          Loading orbital data...
        </div>
        <Line v-else :data="chartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>
