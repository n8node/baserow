<template>
  <div class="layout__col-2-scroll layout__col-2-scroll--white-background">
    <div class="admin-settings">
      <h1>{{ $t('landingAdmin.pageTitle') }}</h1>

      <div class="margin-bottom-2">
        <SegmentControl
          :active-index="localeTabIndex"
          :segments="localeSegments"
          @update:active-index="onLocaleTab"
        />
      </div>

      <div class="margin-bottom-2" style="display: flex; gap: 8px">
        <Button @click="openCreate">
          {{ $t('landingAdmin.addBlock') }}
        </Button>
        <Button type="secondary" tag="a" :href="previewUrl" target="_blank">
          {{ $t('landingAdmin.preview') }}
        </Button>
      </div>

      <div v-if="!blocks || blocks.length === 0" class="margin-bottom-2">
        {{ $t('landingAdmin.noBlocks') }}
      </div>

      <table v-else style="width: 100%; border-collapse: collapse">
        <thead>
          <tr
            style="
              text-align: left;
              border-bottom: 2px solid var(--color-neutral-200);
            "
          >
            <th style="padding: 8px">{{ $t('landingAdmin.order') }}</th>
            <th style="padding: 8px">{{ $t('landingAdmin.blockType') }}</th>
            <th style="padding: 8px">{{ $t('landingAdmin.blockTitle') }}</th>
            <th style="padding: 8px">{{ $t('landingAdmin.enabled') }}</th>
            <th style="padding: 8px"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="block in blocks"
            :key="block.id"
            style="border-bottom: 1px solid var(--color-neutral-100)"
          >
            <td style="padding: 8px">{{ block.order }}</td>
            <td style="padding: 8px">
              <code>{{ block.block_type }}</code>
            </td>
            <td style="padding: 8px">{{ truncate(block.title, 80) }}</td>
            <td style="padding: 8px">{{ block.enabled ? '✓' : '—' }}</td>
            <td style="padding: 8px; white-space: nowrap">
              <Button size="small" type="secondary" @click="openEdit(block)">
                {{ $t('action.edit') }}
              </Button>
              <Button
                size="small"
                type="secondary"
                style="margin-left: 4px"
                @click="duplicateBlock(block)"
              >
                {{ $t('landingAdmin.duplicate') }}
              </Button>
            </td>
          </tr>
        </tbody>
      </table>

      <Modal ref="blockModal" wide @hidden="resetForm">
        <h2 class="margin-bottom-2">
          {{
            editingId
              ? $t('landingAdmin.editBlock')
              : $t('landingAdmin.addBlock')
          }}
        </h2>
        <div style="max-height: 70vh; overflow-y: auto; padding-right: 8px">
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px">
            <FormGroup :label="$t('landingAdmin.order')">
              <FormInput v-model="form.order" type="number" />
            </FormGroup>
            <FormGroup :label="$t('landingAdmin.blockType')">
              <select
                v-model="form.block_type"
                style="
                  width: 100%;
                  padding: 8px;
                  border: 1px solid var(--color-neutral-300);
                  border-radius: 4px;
                "
              >
                <option
                  v-for="bt in blockTypes"
                  :key="bt.value"
                  :value="bt.value"
                >
                  {{ bt.label }}
                </option>
              </select>
            </FormGroup>
          </div>
          <FormGroup>
            <label class="checkbox margin-bottom-0">
              <input v-model="form.enabled" type="checkbox" />
              <span>{{ $t('landingAdmin.enabled') }}</span>
            </label>
          </FormGroup>
          <FormGroup :label="$t('landingAdmin.blockTitle')">
            <FormTextarea v-model="form.title" :rows="2" />
          </FormGroup>
          <FormGroup :label="$t('landingAdmin.subtitle')">
            <FormTextarea v-model="form.subtitle" :rows="2" />
          </FormGroup>
          <FormGroup :label="$t('landingAdmin.body')">
            <FormTextarea v-model="form.body" :rows="4" />
          </FormGroup>
          <FormGroup :label="$t('landingAdmin.imageUrl')">
            <FormInput v-model="form.image_url" />
          </FormGroup>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px">
            <FormGroup :label="$t('landingAdmin.primaryCtaLabel')">
              <FormInput v-model="form.primary_cta_label" />
            </FormGroup>
            <FormGroup :label="$t('landingAdmin.primaryCtaUrl')">
              <FormInput v-model="form.primary_cta_url" />
            </FormGroup>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px">
            <FormGroup :label="$t('landingAdmin.secondaryCtaLabel')">
              <FormInput v-model="form.secondary_cta_label" />
            </FormGroup>
            <FormGroup :label="$t('landingAdmin.secondaryCtaUrl')">
              <FormInput v-model="form.secondary_cta_url" />
            </FormGroup>
          </div>

          <FormGroup :label="$t('landingAdmin.extraData')">
            <FormTextarea
              v-model="extraDataRaw"
              :rows="12"
              style="font-family: monospace; font-size: 12px"
              :placeholder="extraDataPlaceholder"
            />
            <div
              v-if="extraDataError"
              style="color: var(--color-error-400); margin-top: 4px; font-size: 13px"
            >
              {{ extraDataError }}
            </div>
          </FormGroup>
        </div>
        <div class="margin-top-2" style="display: flex; gap: 8px">
          <Button :loading="saving" @click="save">
            {{ $t('action.submit') }}
          </Button>
          <Button v-if="editingId" type="danger" @click="remove">
            {{ $t('landingAdmin.delete') }}
          </Button>
        </div>
      </Modal>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

import Button from '@baserow/modules/core/components/Button'
import FormGroup from '@baserow/modules/core/components/FormGroup'
import FormInput from '@baserow/modules/core/components/FormInput'
import FormTextarea from '@baserow/modules/core/components/FormTextarea'
import Modal from '@baserow/modules/core/components/Modal'
import SegmentControl from '@baserow/modules/core/components/SegmentControl'
import AdminLandingService from '@baserow/modules/core/services/admin/landing'
import { notifyIf } from '@baserow/modules/core/utils/error'

definePageMeta({
  layout: 'app',
  middleware: 'staff',
})

const { $client, $i18n } = useNuxtApp()
const { t } = useI18n()
const config = useRuntimeConfig()

useHead({ title: $i18n.t('landingAdmin.pageTitle') })

const previewUrl = computed(
  () => config.public?.publicWebFrontendUrl || '/'
)

const blockTypes = [
  { value: 'hero', label: 'Hero' },
  { value: 'features_grid', label: 'Features Grid (6 cards)' },
  { value: 'logos', label: 'Client Logos' },
  { value: 'badges', label: 'Badges & Certifications' },
  { value: 'product_tabs', label: 'Product Tabs (screenshots)' },
  { value: 'deployment', label: 'Deployment Options' },
  { value: 'ai_assistant', label: 'AI Assistant (Kuma)' },
  { value: 'how_it_works', label: 'How It Works' },
  { value: 'section_image', label: 'Section + Image' },
  { value: 'automations', label: 'Automations (3 features)' },
  { value: 'templates_grid', label: 'Templates Grid' },
  { value: 'why_baserow', label: 'Why Baserow (features)' },
  { value: 'comparison', label: 'Comparison Table' },
  { value: 'testimonials', label: 'Testimonials' },
  { value: 'cta', label: 'CTA Block' },
  { value: 'footer', label: 'Footer' },
  { value: 'section', label: 'Generic Section' },
]

const adminLocale = ref('ru')
const localeTabIndex = computed(() => (adminLocale.value === 'en' ? 1 : 0))
const localeSegments = computed(() => [
  { label: $i18n.t('landingAdmin.localeTabRu') },
  { label: $i18n.t('landingAdmin.localeTabEn') },
])

function onLocaleTab(index) {
  adminLocale.value = index === 1 ? 'en' : 'ru'
}

const { data: blocks, refresh } = await useAsyncData(
  'admin-landing-blocks',
  async () => {
    const { data } = await AdminLandingService($client).fetchBlocks(
      adminLocale.value
    )
    return data
  },
  { watch: [adminLocale] }
)

const blockModal = ref(null)
const saving = ref(false)
const editingId = ref(null)

const defaultForm = () => ({
  order: 0,
  locale: 'ru',
  enabled: true,
  block_type: 'section',
  title: '',
  subtitle: '',
  body: '',
  image_url: '',
  primary_cta_label: '',
  primary_cta_url: '',
  secondary_cta_label: '',
  secondary_cta_url: '',
  extra_data: {},
})

const form = ref(defaultForm())
const extraDataRaw = ref('{}')
const extraDataError = ref('')

const extraDataPlaceholder = computed(() => {
  const type = form.value.block_type
  const examples = {
    hero: '{"badge": "We\'re proudly European", "self_host_links": [{"label": "Docker", "url": "#"}]}',
    features_grid:
      '{"items": [{"icon": "iconoir-data", "title": "Feature", "description": "Description"}]}',
    logos: '{"items": [{"src": "https://...", "alt": "Company"}]}',
    testimonials:
      '{"items": [{"quote": "...", "name": "John", "role": "CEO", "logo": "https://..."}]}',
    comparison:
      '{"competitor": "Airtable", "items": [{"feature": "Open source", "us": true, "them": false}]}',
    templates_grid:
      '{"items": [{"title": "Template", "image": "https://...", "icon": "iconoir-task-list"}]}',
  }
  return examples[type] || '{}'
})

watch(
  () => form.value.extra_data,
  (v) => {
    extraDataRaw.value = JSON.stringify(v || {}, null, 2)
  },
  { immediate: true }
)

function resetForm() {
  editingId.value = null
  form.value = { ...defaultForm(), locale: adminLocale.value }
  extraDataRaw.value = '{}'
  extraDataError.value = ''
}

function openCreate() {
  resetForm()
  blockModal.value.show()
}

function openEdit(block) {
  editingId.value = block.id
  form.value = {
    order: block.order,
    locale: block.locale,
    enabled: block.enabled,
    block_type: block.block_type,
    title: block.title || '',
    subtitle: block.subtitle || '',
    body: block.body || '',
    image_url: block.image_url || '',
    primary_cta_label: block.primary_cta_label || '',
    primary_cta_url: block.primary_cta_url || '',
    secondary_cta_label: block.secondary_cta_label || '',
    secondary_cta_url: block.secondary_cta_url || '',
    extra_data: block.extra_data || {},
  }
  extraDataRaw.value = JSON.stringify(block.extra_data || {}, null, 2)
  extraDataError.value = ''
  blockModal.value.show()
}

async function duplicateBlock(block) {
  try {
    await AdminLandingService($client).create({
      order: block.order + 1,
      locale: block.locale,
      enabled: false,
      block_type: block.block_type,
      title: block.title || '',
      subtitle: block.subtitle || '',
      body: block.body || '',
      image_url: block.image_url || '',
      primary_cta_label: block.primary_cta_label || '',
      primary_cta_url: block.primary_cta_url || '',
      secondary_cta_label: block.secondary_cta_label || '',
      secondary_cta_url: block.secondary_cta_url || '',
      extra_data: block.extra_data || {},
    })
    await refresh()
  } catch (error) {
    notifyIf(error)
  }
}

function truncate(s, n) {
  if (!s) return ''
  return s.length > n ? `${s.slice(0, n)}…` : s
}

function parseExtraData() {
  try {
    const parsed = JSON.parse(extraDataRaw.value || '{}')
    extraDataError.value = ''
    return parsed
  } catch (e) {
    extraDataError.value = `Invalid JSON: ${e.message}`
    return null
  }
}

async function save() {
  const parsedExtra = parseExtraData()
  if (parsedExtra === null) return

  saving.value = true
  try {
    const payload = {
      ...form.value,
      order: Number(form.value.order) || 0,
      locale: adminLocale.value,
      extra_data: parsedExtra,
    }
    if (editingId.value) {
      await AdminLandingService($client).update(editingId.value, payload)
    } else {
      await AdminLandingService($client).create(payload)
    }
    await refresh()
    blockModal.value.hide()
    resetForm()
  } catch (error) {
    notifyIf(error)
  } finally {
    saving.value = false
  }
}

async function remove() {
  if (!editingId.value) return
  if (!confirm(t('landingAdmin.confirmDelete'))) return
  saving.value = true
  try {
    await AdminLandingService($client).delete(editingId.value)
    await refresh()
    blockModal.value.hide()
    resetForm()
  } catch (error) {
    notifyIf(error)
  } finally {
    saving.value = false
  }
}
</script>
