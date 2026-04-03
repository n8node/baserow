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

      <div class="margin-bottom-2">
        <Button @click="openCreate">
          {{ $t('landingAdmin.addBlock') }}
        </Button>
      </div>

      <div v-if="!blocks || blocks.length === 0" class="margin-bottom-2">
        {{ $t('landingAdmin.noBlocks') }}
      </div>

      <table
        v-else
        style="width: 100%; border-collapse: collapse"
      >
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
            <td style="padding: 8px">
              <Button size="small" type="secondary" @click="openEdit(block)">
                {{ $t('action.edit') }}
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
          <FormGroup :label="$t('landingAdmin.order')">
            <FormInput v-model="form.order" type="number" />
          </FormGroup>
          <FormGroup :label="$t('landingAdmin.blockType')">
            <FormInput
              v-model="form.block_type"
              :placeholder="'hero / section / cta'"
            />
          </FormGroup>
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
          <FormGroup :label="$t('landingAdmin.primaryCtaLabel')">
            <FormInput v-model="form.primary_cta_label" />
          </FormGroup>
          <FormGroup :label="$t('landingAdmin.primaryCtaUrl')">
            <FormInput v-model="form.primary_cta_url" />
          </FormGroup>
          <FormGroup :label="$t('landingAdmin.secondaryCtaLabel')">
            <FormInput v-model="form.secondary_cta_label" />
          </FormGroup>
          <FormGroup :label="$t('landingAdmin.secondaryCtaUrl')">
            <FormInput v-model="form.secondary_cta_url" />
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
import { computed, ref } from 'vue'

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

useHead({ title: $i18n.t('landingAdmin.pageTitle') })

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
})

const form = ref(defaultForm())

function resetForm() {
  editingId.value = null
  form.value = { ...defaultForm(), locale: adminLocale.value }
}

function openCreate() {
  editingId.value = null
  form.value = { ...defaultForm(), locale: adminLocale.value }
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
  }
  blockModal.value.show()
}

function truncate(s, n) {
  if (!s) return ''
  return s.length > n ? `${s.slice(0, n)}…` : s
}

async function save() {
  saving.value = true
  try {
    const payload = {
      ...form.value,
      order: Number(form.value.order) || 0,
      locale: adminLocale.value,
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
