<template>
  <section class="landing-logos">
    <div class="landing-section-container">
      <p v-if="block.title" class="landing-logos__title">{{ block.title }}</p>
      <div class="landing-logos__row">
        <img
          v-for="(item, i) in items"
          :key="i"
          :src="item.src"
          :alt="item.alt || ''"
          class="landing-logos__img"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ block: { type: Object, required: true } })
const items = computed(() => (props.block.extra_data || {}).items || [])
</script>
