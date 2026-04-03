<template>
  <section class="landing-features-grid">
    <div class="landing-section-container">
      <div class="landing-section-header">
        <div class="landing-section-header__line" />
        <h2 v-if="block.title" class="landing-section-header__title">
          {{ block.title }}
        </h2>
        <p v-if="block.subtitle" class="landing-section-header__subtitle">
          {{ block.subtitle }}
        </p>
      </div>
      <div class="landing-features-grid__grid">
        <div
          v-for="(item, i) in items"
          :key="i"
          class="landing-features-grid__card"
        >
          <div
            v-if="item.icon"
            class="landing-features-grid__icon"
            v-html="item.icon_svg || ''"
          />
          <div
            v-else-if="item.icon_emoji"
            class="landing-features-grid__icon-emoji"
          >
            {{ item.icon_emoji }}
          </div>
          <h3 class="landing-features-grid__card-title">{{ item.title }}</h3>
          <p v-if="item.description" class="landing-features-grid__card-desc">
            {{ item.description }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ block: { type: Object, required: true } })
const items = computed(() => (props.block.extra_data || {}).items || [])
</script>
