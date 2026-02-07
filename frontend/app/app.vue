<script setup>
useHead({
  title: "GitPulse",
  titleTemplate: (titleChunk) => {
    return titleChunk ? `${titleChunk} - GitPulse` : "GitPulse";
  },
});
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
