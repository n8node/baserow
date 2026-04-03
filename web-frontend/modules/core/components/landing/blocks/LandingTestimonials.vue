<template>
  <section class="landing-testimonials">
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
      <div class="landing-testimonials__grid">
        <div
          v-for="(item, i) in items"
          :key="i"
          class="landing-testimonials__card"
        >
          <div v-if="item.logo" class="landing-testimonials__logo-wrap">
            <img
              :src="item.logo"
              :alt="item.company || ''"
              class="landing-testimonials__logo"
            />
          </div>
          <p class="landing-testimonials__quote">
            &ldquo;{{ item.quote }}&rdquo;
          </p>
          <div class="landing-testimonials__author">
            <img
              v-if="item.avatar"
              :src="item.avatar"
              :alt="item.name || ''"
              class="landing-testimonials__avatar"
            />
            <div>
              <p class="landing-testimonials__name">{{ item.name }}</p>
              <p v-if="item.role" class="landing-testimonials__role">
                {{ item.role }}
              </p>
            </div>
          </div>
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
