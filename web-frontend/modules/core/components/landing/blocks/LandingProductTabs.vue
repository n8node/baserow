<template>
  <section class="landing-product-tabs">
    <div class="landing-section-container">
      <div class="landing-product-tabs__tabs">
        <button
          v-for="(tab, i) in tabs"
          :key="i"
          class="landing-product-tabs__tab"
          :class="{ 'landing-product-tabs__tab--active': activeTab === i }"
          @click="activeTab = i"
        >
          <span v-if="tab.icon" class="landing-product-tabs__tab-icon">
            {{ tab.icon }}
          </span>
          {{ tab.label }}
          <span v-if="tab.badge" class="landing-product-tabs__tab-badge">
            {{ tab.badge }}
          </span>
        </button>
      </div>
      <div class="landing-product-tabs__content">
        <div class="landing-product-tabs__sidebar">
          <div
            v-for="(item, i) in sidebarItems"
            :key="i"
            class="landing-product-tabs__sidebar-item"
          >
            <span v-if="item.icon" class="landing-product-tabs__sidebar-icon">
              {{ item.icon }}
            </span>
            {{ item.label }}
          </div>
        </div>
        <div class="landing-product-tabs__screenshot">
          <img
            v-if="activeTabData.image"
            :src="activeTabData.image"
            :alt="activeTabData.label || ''"
            class="landing-product-tabs__screenshot-img"
          />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({ block: { type: Object, required: true } })
const extra = computed(() => props.block.extra_data || {})
const tabs = computed(() => extra.value.tabs || [])
const activeTab = ref(0)
const activeTabData = computed(() => tabs.value[activeTab.value] || {})
const sidebarItems = computed(() => activeTabData.value.sidebar || [])
</script>
