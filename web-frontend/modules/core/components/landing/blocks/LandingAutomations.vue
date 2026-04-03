<template>
  <section class="landing-automations">
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
      <div v-if="block.image_url" class="landing-automations__image-wrap">
        <img
          :src="block.image_url"
          alt=""
          class="landing-automations__image"
        />
      </div>
      <div class="landing-automations__features">
        <div
          v-for="(item, i) in items"
          :key="i"
          class="landing-automations__feature"
        >
          <div
            v-if="item.icon"
            class="landing-automations__feature-icon"
          >
            {{ item.icon }}
          </div>
          <h3 class="landing-automations__feature-title">{{ item.title }}</h3>
          <p
            v-if="item.description"
            class="landing-automations__feature-desc"
          >
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
