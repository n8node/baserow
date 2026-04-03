<template>
  <div class="layout__col-2-scroll">
    <div class="admin-settings">
      <h1>{{ $t('billing.admin.title') }}</h1>

      <!-- Payment Providers -->
      <div class="admin-settings__group">
        <h2 class="admin-settings__group-title">
          {{ $t('billing.admin.paymentProviders') }}
        </h2>
        <p class="margin-bottom-2">
          {{ $t('billing.admin.paymentProvidersDescription') }}
        </p>

        <!-- Robokassa -->
        <div class="admin-settings__group" style="border: 1px solid var(--color-neutral-200); border-radius: 6px; padding: 16px; margin-bottom: 16px;">
          <h3 style="margin-top: 0;">Робокасса</h3>
          <div class="admin-settings__item">
            <div class="admin-settings__label">
              <div class="admin-settings__name">{{ $t('billing.admin.status') }}</div>
            </div>
            <div class="admin-settings__control">
              <SwitchInput
                :value="isRobokassaActive"
                @input="toggleProvider('robokassa', $event)"
              >
                {{ isRobokassaActive ? $t('billing.admin.active') : $t('billing.admin.inactive') }}
              </SwitchInput>
            </div>
          </div>
          <div class="admin-settings__item">
            <div class="admin-settings__label">
              <div class="admin-settings__name">Merchant Login</div>
            </div>
            <div class="admin-settings__control">
              <FormInput
                :value="robokassaConfig.merchant_login || ''"
                @input="robokassaConfig.merchant_login = $event"
                @blur="saveProvider('robokassa')"
              />
            </div>
          </div>
          <div class="admin-settings__item">
            <div class="admin-settings__label">
              <div class="admin-settings__name">Password 1</div>
            </div>
            <div class="admin-settings__control">
              <FormInput
                :value="robokassaConfig.password1_input || ''"
                type="password"
                @input="robokassaConfig.password1_input = $event"
                @blur="saveProviderPassword('robokassa', 'password1')"
              />
            </div>
          </div>
          <div class="admin-settings__item">
            <div class="admin-settings__label">
              <div class="admin-settings__name">Password 2</div>
            </div>
            <div class="admin-settings__control">
              <FormInput
                :value="robokassaConfig.password2_input || ''"
                type="password"
                @input="robokassaConfig.password2_input = $event"
                @blur="saveProviderPassword('robokassa', 'password2')"
              />
            </div>
          </div>
          <div class="admin-settings__item">
            <div class="admin-settings__label">
              <div class="admin-settings__name">{{ $t('billing.admin.testMode') }}</div>
            </div>
            <div class="admin-settings__control">
              <SwitchInput
                :value="robokassaConfig.test_mode"
                @input="saveProviderField('robokassa', 'test_mode', $event)"
              >
                {{ $t('settings.enabled') }}
              </SwitchInput>
            </div>
          </div>
        </div>

        <!-- YooKassa -->
        <div class="admin-settings__group" style="border: 1px solid var(--color-neutral-200); border-radius: 6px; padding: 16px; margin-bottom: 16px;">
          <h3 style="margin-top: 0;">ЮKassa</h3>
          <div class="admin-settings__item">
            <div class="admin-settings__label">
              <div class="admin-settings__name">{{ $t('billing.admin.status') }}</div>
            </div>
            <div class="admin-settings__control">
              <SwitchInput
                :value="isYookassaActive"
                @input="toggleProvider('yookassa', $event)"
              >
                {{ isYookassaActive ? $t('billing.admin.active') : $t('billing.admin.inactive') }}
              </SwitchInput>
            </div>
          </div>
          <div class="admin-settings__item">
            <div class="admin-settings__label">
              <div class="admin-settings__name">Shop ID</div>
            </div>
            <div class="admin-settings__control">
              <FormInput
                :value="yookassaConfig.shop_id || ''"
                @input="yookassaConfig.shop_id = $event"
                @blur="saveProvider('yookassa')"
              />
            </div>
          </div>
          <div class="admin-settings__item">
            <div class="admin-settings__label">
              <div class="admin-settings__name">Secret Key</div>
            </div>
            <div class="admin-settings__control">
              <FormInput
                :value="yookassaConfig.secret_key_input || ''"
                type="password"
                @input="yookassaConfig.secret_key_input = $event"
                @blur="saveProviderPassword('yookassa', 'secret_key')"
              />
            </div>
          </div>
          <div class="admin-settings__item">
            <div class="admin-settings__label">
              <div class="admin-settings__name">{{ $t('billing.admin.testMode') }}</div>
            </div>
            <div class="admin-settings__control">
              <SwitchInput
                :value="yookassaConfig.test_mode"
                @input="saveProviderField('yookassa', 'test_mode', $event)"
              >
                {{ $t('settings.enabled') }}
              </SwitchInput>
            </div>
          </div>
        </div>
      </div>

      <!-- Plans -->
      <div class="admin-settings__group">
        <h2 class="admin-settings__group-title">
          {{ $t('billing.admin.plans') }}
          <Button size="small" style="margin-left: 16px;" @click="showCreatePlan = true">
            {{ $t('billing.admin.createPlan') }}
          </Button>
        </h2>

        <div v-if="adminPlans.length === 0" class="margin-bottom-2">
          {{ $t('billing.admin.noPlans') }}
        </div>

        <table v-else class="admin-settings__table" style="width: 100%; border-collapse: collapse;">
          <thead>
            <tr style="text-align: left; border-bottom: 2px solid var(--color-neutral-200);">
              <th style="padding: 8px;">{{ $t('billing.admin.planName') }}</th>
              <th style="padding: 8px;">Slug</th>
              <th style="padding: 8px;">{{ $t('billing.admin.priceMonthly') }}</th>
              <th style="padding: 8px;">{{ $t('billing.admin.maxRows') }}</th>
              <th style="padding: 8px;">{{ $t('billing.admin.storage') }}</th>
              <th style="padding: 8px;">{{ $t('billing.admin.default') }}</th>
              <th style="padding: 8px;">{{ $t('billing.admin.activeState') }}</th>
              <th style="padding: 8px;"></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="plan in adminPlans"
              :key="plan.id"
              style="border-bottom: 1px solid var(--color-neutral-100);"
            >
              <td style="padding: 8px;">{{ plan.name }}</td>
              <td style="padding: 8px;"><code>{{ plan.slug }}</code></td>
              <td style="padding: 8px;">{{ plan.price_monthly }} {{ plan.currency }}</td>
              <td style="padding: 8px;">{{ plan.max_rows_per_workspace || '∞' }}</td>
              <td style="padding: 8px;">{{ plan.max_storage_mb ? plan.max_storage_mb + ' MB' : '∞' }}</td>
              <td style="padding: 8px;">
                <Badge v-if="plan.is_default" color="green" bold>★</Badge>
              </td>
              <td style="padding: 8px;">
                <Badge :color="plan.is_active ? 'green' : 'neutral'" bold>
                  {{ plan.is_active ? $t('billing.admin.active') : $t('billing.admin.inactive') }}
                </Badge>
              </td>
              <td style="padding: 8px;">
                <Button size="small" type="secondary" @click="editPlan(plan)">
                  {{ $t('action.edit') }}
                </Button>
                <Button
                  v-if="!plan.is_default"
                  size="small"
                  type="secondary"
                  style="margin-left: 4px;"
                  @click="setDefault(plan)"
                >
                  ★
                </Button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Plan Edit Modal -->
      <Modal :visible="showEditPlan || showCreatePlan" @hidden="closePlanModal">
        <h2>{{ showCreatePlan ? $t('billing.admin.createPlan') : $t('billing.admin.editPlan') }}</h2>
        <div style="max-height: 70vh; overflow-y: auto; padding-right: 8px;">
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
            <FormInput v-model="planForm.max_rows_per_workspace" type="number" :placeholder="$t('billing.admin.unlimited')" />
          </FormGroup>
          <FormGroup :label="$t('billing.admin.storage') + ' (MB)'">
            <FormInput v-model="planForm.max_storage_mb" type="number" :placeholder="$t('billing.admin.unlimited')" />
          </FormGroup>
          <FormGroup :label="$t('billing.admin.maxWorkspaces')">
            <FormInput v-model="planForm.max_workspaces" type="number" :placeholder="$t('billing.admin.unlimited')" />
          </FormGroup>
          <FormGroup :label="$t('billing.admin.maxCollaborators')">
            <FormInput v-model="planForm.max_collaborators_per_workspace" type="number" :placeholder="$t('billing.admin.unlimited')" />
          </FormGroup>
          <FormGroup :label="$t('billing.admin.maxAutomations')">
            <FormInput v-model="planForm.max_automations" type="number" :placeholder="$t('billing.admin.unlimited')" />
          </FormGroup>
          <FormGroup :label="$t('billing.admin.maxApiCalls')">
            <FormInput v-model="planForm.max_api_calls_per_month" type="number" :placeholder="$t('billing.admin.unlimited')" />
          </FormGroup>

          <h3>{{ $t('billing.admin.features') }}</h3>
          <div v-for="feat in availableFeatures" :key="feat.key" style="margin-bottom: 8px;">
            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
              <input
                type="checkbox"
                :checked="(planForm.features || []).includes(feat.key)"
                @change="toggleFeature(feat.key)"
              />
              {{ feat.name }} <code style="font-size: 11px;">({{ feat.key }})</code>
            </label>
          </div>

          <div class="admin-settings__item" style="margin-top: 16px;">
            <SwitchInput
              :value="planForm.is_active"
              @input="planForm.is_active = $event"
            >
              {{ $t('billing.admin.activeState') }}
            </SwitchInput>
          </div>
        </div>
        <div style="margin-top: 16px; display: flex; gap: 8px; justify-content: flex-end;">
          <Button type="secondary" @click="closePlanModal">{{ $t('action.cancel') }}</Button>
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

const { $client } = useNuxtApp()
const { t: $t } = useI18n()
const store = useStore()

const app = { $client }

const showEditPlan = ref(false)
const showCreatePlan = ref(false)
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

const robokassaConfig = reactive({
  merchant_login: '',
  password1_input: '',
  password2_input: '',
  test_mode: true,
})

const yookassaConfig = reactive({
  shop_id: '',
  secret_key_input: '',
  test_mode: true,
})

const adminPlans = computed(() => store.getters['billing/getAdminPlans'])
const adminProviders = computed(() => store.getters['billing/getAdminProviders'])
const availableFeatures = computed(() => store.getters['billing/getAvailableFeatures'])

const isRobokassaActive = computed(() => {
  const p = adminProviders.value.find((pr) => pr.provider_type === 'robokassa')
  return p?.is_active || false
})
const isYookassaActive = computed(() => {
  const p = adminProviders.value.find((pr) => pr.provider_type === 'yookassa')
  return p?.is_active || false
})

onMounted(async () => {
  try {
    await Promise.all([
      store.dispatch('billing/adminFetchPlans', { app }),
      store.dispatch('billing/adminFetchProviders', { app }),
      store.dispatch('billing/adminFetchAvailableFeatures', { app }),
    ])
    syncProviderConfigs()
  } catch (e) {
    notifyIf(e)
  }
})

function syncProviderConfigs() {
  const robo = adminProviders.value.find((p) => p.provider_type === 'robokassa')
  if (robo) {
    robokassaConfig.merchant_login = robo.merchant_login || ''
    robokassaConfig.test_mode = robo.test_mode ?? true
  }
  const yoo = adminProviders.value.find((p) => p.provider_type === 'yookassa')
  if (yoo) {
    yookassaConfig.shop_id = yoo.shop_id || ''
    yookassaConfig.test_mode = yoo.test_mode ?? true
  }
}

async function toggleProvider(type, active) {
  try {
    if (active) {
      await store.dispatch('billing/adminActivateProvider', { app, providerType: type })
    } else {
      await store.dispatch('billing/adminDeactivateProvider', { app, providerType: type })
    }
    syncProviderConfigs()
  } catch (e) {
    notifyIf(e)
  }
}

async function saveProvider(type) {
  try {
    const data = type === 'robokassa'
      ? { merchant_login: robokassaConfig.merchant_login }
      : { shop_id: yookassaConfig.shop_id }
    await store.dispatch('billing/adminUpdateProvider', { app, providerType: type, providerData: data })
  } catch (e) {
    notifyIf(e)
  }
}

async function saveProviderPassword(type, field) {
  const inputField = type === 'robokassa'
    ? robokassaConfig[field + '_input']
    : yookassaConfig[field + '_input']
  if (!inputField) return
  try {
    await store.dispatch('billing/adminUpdateProvider', {
      app,
      providerType: type,
      providerData: { [field]: inputField },
    })
  } catch (e) {
    notifyIf(e)
  }
}

async function saveProviderField(type, field, value) {
  try {
    if (type === 'robokassa') robokassaConfig[field] = value
    else yookassaConfig[field] = value
    await store.dispatch('billing/adminUpdateProvider', {
      app,
      providerType: type,
      providerData: { [field]: value },
    })
  } catch (e) {
    notifyIf(e)
  }
}

function editPlan(plan) {
  editingPlanId.value = plan.id
  Object.assign(planForm, {
    ...plan,
    features: [...(plan.features || [])],
  })
  showEditPlan.value = true
}

function closePlanModal() {
  showEditPlan.value = false
  showCreatePlan.value = false
  editingPlanId.value = null
  resetPlanForm()
}

function resetPlanForm() {
  Object.assign(planForm, {
    name: '', slug: '', description: '', order: 0,
    price_monthly: 0, price_yearly: 0, currency: 'RUB',
    max_rows_per_workspace: null, max_storage_mb: null,
    max_workspaces: null, max_collaborators_per_workspace: null,
    max_automations: null, max_api_calls_per_month: null,
    max_file_upload_size_mb: null, features: [],
    is_active: true, is_default: false,
  })
}

function toggleFeature(key) {
  const features = planForm.features || []
  const idx = features.indexOf(key)
  if (idx === -1) features.push(key)
  else features.splice(idx, 1)
  planForm.features = [...features]
}

async function savePlan() {
  try {
    const data = { ...planForm }
    // Convert empty strings to null for nullable int fields
    for (const f of [
      'max_rows_per_workspace', 'max_storage_mb', 'max_workspaces',
      'max_collaborators_per_workspace', 'max_automations',
      'max_api_calls_per_month', 'max_file_upload_size_mb',
    ]) {
      if (data[f] === '' || data[f] === undefined) data[f] = null
      else data[f] = data[f] !== null ? parseInt(data[f]) : null
    }
    data.order = parseInt(data.order) || 0
    data.price_monthly = parseFloat(data.price_monthly) || 0
    data.price_yearly = parseFloat(data.price_yearly) || 0

    if (showCreatePlan.value) {
      await store.dispatch('billing/adminCreatePlan', { app, planData: data })
    } else {
      await store.dispatch('billing/adminUpdatePlan', {
        app, planId: editingPlanId.value, planData: data,
      })
    }
    closePlanModal()
  } catch (e) {
    notifyIf(e)
  }
}

async function setDefault(plan) {
  try {
    await store.dispatch('billing/adminSetDefaultPlan', { app, planId: plan.id })
  } catch (e) {
    notifyIf(e)
  }
}
</script>
