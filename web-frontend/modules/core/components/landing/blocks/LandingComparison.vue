<template>
  <section class="landing-comparison">
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
      <div class="landing-comparison__table">
        <div class="landing-comparison__header">
          <div class="landing-comparison__col landing-comparison__col--us">
            <img
              v-if="extra.our_logo"
              :src="extra.our_logo"
              alt=""
              class="landing-comparison__logo"
            />
            <span v-else class="landing-comparison__brand">{{
              extra.our_name || 'Baserow'
            }}</span>
          </div>
          <div class="landing-comparison__col landing-comparison__col--them">
            <img
              v-if="extra.their_logo"
              :src="extra.their_logo"
              alt=""
              class="landing-comparison__logo"
            />
            <span v-else class="landing-comparison__brand">{{
              extra.competitor || 'Competitor'
            }}</span>
          </div>
        </div>
        <div
          v-for="(item, i) in items"
          :key="i"
          class="landing-comparison__row"
        >
          <div class="landing-comparison__col landing-comparison__col--us">
            <span v-if="item.us === true" class="landing-comparison__check">&#10003;</span>
            <span v-else-if="item.us === false" class="landing-comparison__cross">&#10005;</span>
            <span v-else>{{ item.us }}</span>
            <span class="landing-comparison__feature-text">{{
              item.us_text || item.feature
            }}</span>
          </div>
          <div class="landing-comparison__col landing-comparison__col--them">
            <span v-if="item.them === true" class="landing-comparison__check">&#10003;</span>
            <span v-else-if="item.them === false" class="landing-comparison__cross">&#10005;</span>
            <span v-else>{{ item.them }}</span>
            <span class="landing-comparison__feature-text">{{
              item.them_text || item.feature
            }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ block: { type: Object, required: true } })
const extra = computed(() => props.block.extra_data || {})
const items = computed(() => extra.value.items || [])
</script>
