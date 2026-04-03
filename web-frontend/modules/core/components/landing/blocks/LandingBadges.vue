<template>
  <section class="landing-badges">
    <div class="landing-section-container">
      <div v-if="ratings.length" class="landing-badges__group">
        <p v-if="ratingsTitle" class="landing-badges__group-title">
          {{ ratingsTitle }}
        </p>
        <div class="landing-badges__row">
          <img
            v-for="(b, i) in ratings"
            :key="'r' + i"
            :src="b.src"
            :alt="b.alt || ''"
            class="landing-badges__badge"
          />
        </div>
      </div>
      <div v-if="certs.length" class="landing-badges__group">
        <p v-if="certsTitle" class="landing-badges__group-title">
          {{ certsTitle }}
        </p>
        <div class="landing-badges__row">
          <div
            v-for="(c, i) in certs"
            :key="'c' + i"
            class="landing-badges__cert"
          >
            <img
              v-if="c.src"
              :src="c.src"
              :alt="c.alt || ''"
              class="landing-badges__cert-img"
            />
            <span v-if="c.label" class="landing-badges__cert-label">{{
              c.label
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
const ratings = computed(() => extra.value.ratings || [])
const certs = computed(() => extra.value.certifications || [])
const ratingsTitle = computed(() => extra.value.ratings_title || '')
const certsTitle = computed(() => extra.value.certifications_title || '')
</script>
