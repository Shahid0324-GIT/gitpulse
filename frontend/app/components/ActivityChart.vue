<script setup lang="ts">
import { computed } from "vue";
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  type ChartData,
  type ChartOptions,
} from "chart.js";

// Register Chart.js components
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
);

const props = defineProps<{
  events: GithubEvent[];
}>();

const chartData = computed<ChartData<"bar">>(() => {
  let pushCount = 0;
  let watchCount = 0;
  let createCount = 0;
  let otherCount = 0;

  props.events.forEach((event) => {
    if (event.event_type === "PushEvent") {
      pushCount++;
    } else if (event.event_type === "WatchEvent") {
      watchCount++;
    } else if (event.event_type === "CreateEvent") {
      createCount++;
    } else {
      otherCount++;
    }
  });

  return {
    labels: ["Push", "Star", "Create", "Other"],
    datasets: [
      {
        label: "Events",
        data: [pushCount, watchCount, createCount, otherCount],
        backgroundColor: ["#3b82f6", "#fbbf24", "#10b981", "#94a3b8"],
        borderRadius: 6,
      },
    ],
  };
});

const chartOptions: ChartOptions<"bar"> = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    y: {
      grid: { color: "#334155" },
      ticks: { color: "#94a3b8" },
      beginAtZero: true,
    },
    x: {
      grid: { display: false },
      ticks: { color: "#94a3b8" },
    },
  },
};
</script>

<template>
  <div class="h-full w-full relative">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>
