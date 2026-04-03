<template>
  <section class="landing-deployment">
    <div class="landing-section-container">
      <div class="landing-deployment__card">
        <p class="landing-deployment__label">{{ block.title }}</p>
        <div class="landing-deployment__options">
          <div
            v-for="(opt, i) in options"
            :key="i"
            class="landing-deployment__option"
          >
            <div v-if="opt.icon" class="landing-deployment__option-icon">
              {{ opt.icon }}
            </div>
            <p class="landing-deployment__option-title">{{ opt.title }}</p>
            <p
              v-if="opt.description"
              class="landing-deployment__option-desc"
            >
              {{ opt.description }}
            </p>
            <div v-if="opt.logos && opt.logos.length" class="landing-deployment__option-logos">
              <img
                v-for="(logo, j) in opt.logos"
                :key="j"
                :src="logo"
                alt=""
                class="landing-deployment__option-logo"
              />
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
const options = computed(() => (props.block.extra_data || {}).options || [])
</script>
