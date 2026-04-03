<template>
  <section class="landing-how-it-works">
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
      <div v-if="block.image_url" class="landing-how-it-works__diagram">
        <img
          :src="block.image_url"
          alt=""
          class="landing-how-it-works__diagram-img"
        />
      </div>
      <div v-else-if="columns.length" class="landing-how-it-works__columns">
        <div
          v-for="(col, i) in columns"
          :key="i"
          class="landing-how-it-works__column"
        >
          <div class="landing-how-it-works__column-header">
            {{ col.title }}
          </div>
          <div
            v-for="(item, j) in col.items || []"
            :key="j"
            class="landing-how-it-works__item"
          >
            <span v-if="item.icon" class="landing-how-it-works__item-icon">
              {{ item.icon }}
            </span>
            <div>
              <p class="landing-how-it-works__item-title">{{ item.title }}</p>
              <p
                v-if="item.description"
                class="landing-how-it-works__item-desc"
              >
                {{ item.description }}
              </p>
              <div v-if="item.tags && item.tags.length" class="landing-how-it-works__tags">
                <span
                  v-for="(tag, k) in item.tags"
                  :key="k"
                  class="landing-how-it-works__tag"
                >
                  {{ tag }}
                </span>
              </div>
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
const columns = computed(() => (props.block.extra_data || {}).columns || [])
</script>
