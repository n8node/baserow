<template>
  <NuxtPage />
</template>

<script setup>
definePageMeta({
  name: 'billing-root',
  layout: 'app',
  middleware: [
    'settings',
    'authenticated',
    'workspacesAndApplications',
    'pendingJobs',
  ],
})
</script>
