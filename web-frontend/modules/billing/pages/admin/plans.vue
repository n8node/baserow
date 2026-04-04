<template>
  <div class="layout__col-2-scroll layout__col-2-scroll--white-background">
    <div class="admin-settings">
      <h1>
        {{ $t('billing.admin.plans') }}
        <Button size="small" style="margin-left: 16px" @click="openCreatePlan">
          {{ $t('billing.admin.createPlan') }}
        </Button>
      </h1>

      <div v-if="adminPlans.length === 0" class="margin-bottom-2">
        {{ $t('billing.admin.noPlans') }}
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
            <th style="padding: 8px">{{ $t('billing.admin.planName') }}</th>
            <th style="padding: 8px">Slug</th>
            <th style="padding: 8px">{{ $t('billing.admin.priceMonthly') }}</th>
            <th style="padding: 8px">{{ $t('billing.admin.maxRows') }}</th>
            <th style="padding: 8px">{{ $t('billing.admin.storage') }}</th>
            <th style="padding: 8px">{{ $t('billing.admin.default') }}</th>
            <th style="padding: 8px">{{ $t('billing.admin.activeState') }}</th>
            <th style="padding: 8px">{{ $t('billing.admin.subscribers') }}</th>
            <th style="padding: 8px"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="plan in adminPlans"
            :key="plan.id"
            style="border-bottom: 1px solid var(--color-neutral-100)"
          >
            <td style="padding: 8px">{{ plan.name }}</td>
            <td style="padding: 8px">
              <code>{{ plan.slug }}</code>
            </td>
            <td style="padding: 8px">
              {{ plan.price_monthly }} {{ plan.currency }}
            </td>
            <td style="padding: 8px">
              {{ plan.max_rows_per_workspace || '∞' }}
            </td>
            <td style="padding: 8px">
              {{
                plan.max_storage_mb ? plan.max_storage_mb + ' MB' : '∞'
              }}
            </td>
            <td style="padding: 8px">
              <Badge v-if="plan.is_default" color="green" bold>★</Badge>
            </td>
            <td style="padding: 8px">
              <Badge
                :color="plan.is_active ? 'green' : 'neutral'"
                bold
              >
                {{
                  plan.is_active
                    ? $t('billing.admin.active')
                    : $t('billing.admin.inactive')
                }}
              </Badge>
            </td>
            <td style="padding: 8px">{{ plan.subscription_count ?? '—' }}</td>
            <td style="padding: 8px">
              <Button
                size="small"
                type="secondary"
                @click="openEditPlan(plan)"
              >
                {{ $t('action.edit') }}
              </Button>
              <Button
                v-if="!plan.is_default"
                size="small"
                type="secondary"
                style="margin-left: 4px"
                @click="setDefault(plan)"
              >
                ★
              </Button>
              <Button
                v-if="!plan.is_default"
                size="small"
                type="danger"
                style="margin-left: 4px"
                :disabled="!canDeletePlan(plan)"
                :title="deletePlanDisabledTitle(plan)"
                @click="deletePlan(plan)"
              >
                {{ $t('billing.admin.deletePlan') }}
              </Button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Plan Edit / Create Modal -->
      <Modal ref="planModal">
        <h2>
          {{
            isCreating
              ? $t('billing.admin.createPlan')
              : $t('billing.admin.editPlan')
          }}
        </h2>
        <div
          style="max-height: 70vh; overflow-y: auto; padding-right: 8px"
        >
          <FormGroup :label="$t('billing.admin.planName')">
            <FormInput v-model="planForm.name" />
          </FormGroup>
          <FormGroup label="Slug">
            <FormInput v-model="planForm.slug" />
          </FormGroup>
          <FormGroup :label="$t('billing.admin.description')">
            <FormInput v-model="planForm.description" />
          </FormGroup>
          <FormGroup :label="$t('billing.admin.order')">
            <FormInput v-model="planForm.order" type="number" />
          </FormGroup>
          <FormGroup :label="$t('billing.admin.priceMonthly')">
            <FormInput v-model="planForm.price_monthly" type="number" />
          </FormGroup>
          <FormGroup :label="$t('billing.admin.priceYearly')">
            <FormInput v-model="planForm.price_yearly" type="number" />
          </FormGroup>

          <h3>{{ $t('billing.admin.limits') }}</h3>
          <FormGroup :label="$t('billing.admin.maxRows')">
            <FormInput
              v-model="planForm.max_rows_per_workspace"
              type="number"
              :placeholder="$t('billing.admin.unlimited')"
            />
          </FormGroup>
          <FormGroup :label="$t('billing.admin.storage') + ' (MB)'">
            <FormInput
              v-model="planForm.max_storage_mb"
              type="number"
              :placeholder="$t('billing.admin.unlimited')"
            />
          </FormGroup>
          <FormGroup :label="$t('billing.admin.maxWorkspaces')">
            <FormInput
              v-model="planForm.max_workspaces"
              type="number"
              :placeholder="$t('billing.admin.unlimited')"
            />
          </FormGroup>
          <FormGroup :label="$t('billing.admin.maxCollaborators')">
            <FormInput
              v-model="planForm.max_collaborators_per_workspace"
              type="number"
              :placeholder="$t('billing.admin.unlimited')"
            />
          </FormGroup>
          <FormGroup :label="$t('billing.admin.maxAutomations')">
            <FormInput
              v-model="planForm.max_automations"
              type="number"
              :placeholder="$t('billing.admin.unlimited')"
            />
          </FormGroup>
          <FormGroup :label="$t('billing.admin.maxApiCalls')">
            <FormInput
              v-model="planForm.max_api_calls_per_month"
              type="number"
              :placeholder="$t('billing.admin.unlimited')"
            />
          </FormGroup>

          <h3>{{ $t('billing.admin.features') }}</h3>
          <div
            v-for="feat in availableFeatures"
            :key="feat.key"
            style="margin-bottom: 8px"
          >
            <label
              style="
                display: flex;
                align-items: center;
                gap: 8px;
                cursor: pointer;
              "
            >
              <input
                type="checkbox"
                :checked="(planForm.features || []).includes(feat.key)"
                @change="toggleFeature(feat.key)"
              />
              {{ feat.name }}
              <code style="font-size: 11px">({{ feat.key }})</code>
            </label>
          </div>

          <div class="admin-settings__item" style="margin-top: 16px">
            <SwitchInput
              :value="planForm.is_active"
              @input="planForm.is_active = $event"
            >
              {{ $t('billing.admin.activeState') }}
            </SwitchInput>
          </div>
        </div>
        <div
          style="
            margin-top: 16px;
            display: flex;
            gap: 8px;
            align-items: center;
            flex-wrap: wrap;
          "
        >
          <Button
            v-if="!isCreating && !planForm.is_default"
            type="danger"
            :disabled="!canDeletePlan(planForm)"
            :title="deletePlanDisabledTitle(planForm)"
            @click="deletePlanFromModal"
          >
            {{ $t('billing.admin.deletePlan') }}
          </Button>
          <div style="flex: 1; min-width: 8px"></div>
          <Button type="secondary" @click="closePlanModal">
            {{ $t('action.cancel') }}
          </Button>
          <Button @click="savePlan">{{ $t('action.save') }}</Button>
        </div>
      </Modal>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useNuxtApp } from '#app'
import { useStore } from 'vuex'
import { notifyIf } from '@baserow/modules/core/utils/error'

definePageMeta({
  layout: 'app',
  middleware: 'staff',
})

const { $client, $i18n } = useNuxtApp()
useHead({ title: $i18n.t('billing.admin.plans') })

const store = useStore()
const app = { $client }

const PLAN_WRITABLE_FIELDS = [
  'slug',
  'name',
  'description',
  'is_default',
  'is_active',
  'order',
  'price_monthly',
  'price_yearly',
  'currency',
  'max_rows_per_workspace',
  'max_storage_mb',
  'max_workspaces',
  'max_collaborators_per_workspace',
  'max_automations',
  'max_api_calls_per_month',
  'max_file_upload_size_mb',
  'features',
]

const planModal = ref(null)
const isCreating = ref(false)
const editingPlanId = ref(null)

const planForm = reactive({
  name: '',
  slug: '',
  description: '',
  order: 0,
  price_monthly: 0,
  price_yearly: 0,
  currency: 'RUB',
  max_rows_per_workspace: null,
  max_storage_mb: null,
  max_workspaces: null,
  max_collaborators_per_workspace: null,
  max_automations: null,
  max_api_calls_per_month: null,
  max_file_upload_size_mb: null,
  features: [],
  is_active: true,
  is_default: false,
})

const adminPlans = computed(() => store.getters['billing/getAdminPlans'])
const availableFeatures = computed(
  () => store.getters['billing/getAvailableFeatures']
)

onMounted(async () => {
  try {
    await Promise.all([
      store.dispatch('billing/adminFetchPlans', { app }),
      store.dispatch('billing/adminFetchAvailableFeatures', { app }),
    ])
  } catch (e) {
    notifyIf(e)
  }
})

function resetPlanForm() {
  Object.assign(planForm, {
    name: '',
    slug: '',
    description: '',
    order: 0,
    price_monthly: 0,
    price_yearly: 0,
    currency: 'RUB',
    max_rows_per_workspace: null,
    max_storage_mb: null,
    max_workspaces: null,
    max_collaborators_per_workspace: null,
    max_automations: null,
    max_api_calls_per_month: null,
    max_file_upload_size_mb: null,
    features: [],
    is_active: true,
    is_default: false,
  })
}

function openCreatePlan() {
  isCreating.value = true
  editingPlanId.value = null
  resetPlanForm()
  planModal.value.show()
}

function openEditPlan(plan) {
  isCreating.value = false
  editingPlanId.value = plan.id
  Object.assign(planForm, {
    ...plan,
    features: [...(plan.features || [])],
  })
  planModal.value.show()
}

function closePlanModal() {
  planModal.value.hide()
  editingPlanId.value = null
  isCreating.value = false
  resetPlanForm()
}

function toggleFeature(key) {
  const features = planForm.features || []
  const idx = features.indexOf(key)
  if (idx === -1) features.push(key)
  else features.splice(idx, 1)
  planForm.features = [...features]
}

function normalizeNullableInt(value) {
  if (value === '' || value === undefined || value === null) return null
  if (typeof value === 'number' && Number.isFinite(value)) {
    return Math.trunc(value)
  }
  const n = parseInt(String(value), 10)
  return Number.isNaN(n) ? null : n
}

function buildPlanPayload() {
  const raw = { ...planForm }
  const data = {}
  for (const key of PLAN_WRITABLE_FIELDS) {
    if (Object.prototype.hasOwnProperty.call(raw, key)) {
      data[key] = raw[key]
    }
  }
  const intFields = [
    'max_rows_per_workspace',
    'max_storage_mb',
    'max_workspaces',
    'max_collaborators_per_workspace',
    'max_automations',
    'max_api_calls_per_month',
    'max_file_upload_size_mb',
  ]
  for (const f of intFields) {
    data[f] = normalizeNullableInt(data[f])
  }
  data.order = normalizeNullableInt(data.order) ?? 0
  data.price_monthly = parseFloat(data.price_monthly) || 0
  data.price_yearly = parseFloat(data.price_yearly) || 0
  if (!Array.isArray(data.features)) {
    data.features = []
  }
  return data
}

function handleBillingApiError(e) {
  if (e?.handler) {
    e.handler.notifyIf()
  } else {
    console.error('[billing] Unhandled error:', e)
    store.dispatch(
      'toast/error',
      {
        title: $i18n.t('clientHandler.notCompletedTitle'),
        message: e?.message || String(e),
      },
      { root: true }
    )
  }
}

function planSubscriberCount(plan) {
  if (!plan) return null
  const n = plan.subscription_count
  if (n == null || n === '') return null
  const num = Number(n)
  return Number.isFinite(num) ? num : null
}

function canDeletePlan(plan) {
  if (!plan || plan.is_default) return false
  const c = planSubscriberCount(plan)
  if (c === null) return true
  return c === 0
}

function deletePlanDisabledTitle(plan) {
  if (!plan || plan.is_default || canDeletePlan(plan)) return ''
  return $i18n.t('billing.admin.deletePlanDisabledHint')
}

async function deletePlan(plan) {
  if (!canDeletePlan(plan)) return
  if (!confirm($i18n.t('billing.admin.confirmDeletePlan'))) return
  try {
    await store.dispatch('billing/adminDeletePlan', {
      app,
      planId: plan.id,
    })
    if (editingPlanId.value === plan.id) {
      closePlanModal()
    }
  } catch (e) {
    handleBillingApiError(e)
  }
}

async function deletePlanFromModal() {
  if (!canDeletePlan(planForm)) return
  const plan = { id: planForm.id, subscription_count: planForm.subscription_count }
  await deletePlan(plan)
}

async function savePlan() {
  try {
    const data = buildPlanPayload()
    if (isCreating.value) {
      await store.dispatch('billing/adminCreatePlan', {
        app,
        planData: data,
      })
    } else {
      await store.dispatch('billing/adminUpdatePlan', {
        app,
        planId: editingPlanId.value,
        planData: data,
      })
    }
    closePlanModal()
  } catch (e) {
    handleBillingApiError(e)
  }
}

async function setDefault(plan) {
  try {
    await store.dispatch('billing/adminSetDefaultPlan', {
      app,
      planId: plan.id,
    })
  } catch (e) {
    notifyIf(e)
  }
}
</script>
