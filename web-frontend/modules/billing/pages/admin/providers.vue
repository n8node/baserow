<template>
  <div class="layout__col-2-scroll layout__col-2-scroll--white-background">
    <div class="admin-settings">
      <h1>{{ $t('billing.admin.paymentProviders') }}</h1>
      <p class="margin-bottom-2">
        {{ $t('billing.admin.paymentProvidersDescription') }}
      </p>

      <!-- Robokassa -->
      <div class="admin-settings__group">
        <h2 class="admin-settings__group-title">Робокасса</h2>
        <div class="admin-settings__item">
          <div class="admin-settings__label">
            <div class="admin-settings__name">
              {{ $t('billing.admin.status') }}
            </div>
          </div>
          <div class="admin-settings__control">
            <SwitchInput
              :value="isRobokassaActive"
              @input="toggleProvider('robokassa', $event)"
            >
              {{
                isRobokassaActive
                  ? $t('billing.admin.active')
                  : $t('billing.admin.inactive')
              }}
            </SwitchInput>
          </div>
        </div>
        <div class="admin-settings__item">
          <div class="admin-settings__label">
            <div class="admin-settings__name">Merchant Login</div>
          </div>
          <div class="admin-settings__control">
            <FormInput
              :value="robokassaConfig.merchant_login"
              @input="robokassaConfig.merchant_login = $event"
              @blur="saveProvider('robokassa')"
            />
          </div>
        </div>
        <div class="admin-settings__item">
          <div class="admin-settings__label">
            <div class="admin-settings__name">Password 1</div>
            <div class="admin-settings__description">
              {{ $t('billing.admin.robokassaPasswordHint') }}
            </div>
          </div>
          <div class="admin-settings__control">
            <FormInput
              :value="robokassaConfig.password1_input"
              @focus="onPasswordFocus('robokassa', 'password1')"
              @input="robokassaConfig.password1_input = $event"
              @blur="saveProviderPassword('robokassa', 'password1')"
            />
          </div>
        </div>
        <div class="admin-settings__item">
          <div class="admin-settings__label">
            <div class="admin-settings__name">Password 2</div>
            <div class="admin-settings__description">
              {{ $t('billing.admin.robokassaPasswordHint') }}
            </div>
          </div>
          <div class="admin-settings__control">
            <FormInput
              :value="robokassaConfig.password2_input"
              @focus="onPasswordFocus('robokassa', 'password2')"
              @input="robokassaConfig.password2_input = $event"
              @blur="saveProviderPassword('robokassa', 'password2')"
            />
          </div>
        </div>
        <div class="admin-settings__item">
          <div class="admin-settings__label">
            <div class="admin-settings__name">
              {{ $t('billing.admin.testMode') }}
            </div>
            <div class="admin-settings__description">
              {{ $t('billing.admin.robokassaTestModeHint') }}
            </div>
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
        <div class="admin-settings__item">
          <div class="admin-settings__label">
            <div class="admin-settings__name">
              {{ $t('billing.admin.robokassaHashAlgorithm') }}
            </div>
            <div class="admin-settings__description">
              {{ $t('billing.admin.robokassaHashAlgorithmDescription') }}
            </div>
          </div>
          <div class="admin-settings__control">
            <select
              :value="robokassaConfig.hash_algorithm"
              style="
                width: 100%;
                padding: 8px;
                border: 1px solid var(--color-neutral-300);
                border-radius: 4px;
              "
              @change="
                saveProviderField(
                  'robokassa',
                  'hash_algorithm',
                  $event.target.value
                )
              "
            >
              <option
                v-for="opt in robokassaHashOptions"
                :key="opt.value"
                :value="opt.value"
              >
                {{ opt.name }}
              </option>
            </select>
          </div>
        </div>
        <div class="admin-settings__item">
          <div class="admin-settings__label">
            <div class="admin-settings__name">
              {{ $t('billing.admin.robokassaFiscalization') }}
            </div>
            <div class="admin-settings__description">
              {{ $t('billing.admin.robokassaFiscalizationDescription') }}
            </div>
          </div>
          <div class="admin-settings__control">
            <SwitchInput
              :value="robokassaConfig.fiscalization_enabled"
              @input="
                saveProviderField('robokassa', 'fiscalization_enabled', $event)
              "
            >
              {{ $t('settings.enabled') }}
            </SwitchInput>
          </div>
        </div>
        <div class="admin-settings__item">
          <div class="admin-settings__label">
            <div class="admin-settings__name">
              {{ $t('billing.admin.robokassaResultUrl') }}
            </div>
            <div class="admin-settings__description">
              {{ $t('billing.admin.robokassaResultUrlDescription') }}
            </div>
          </div>
          <div class="admin-settings__control">
            <template v-if="robokassaResultUrl">
              {{ robokassaResultUrl }}
              <a
                class="licenses__instance-id-copy"
                @click.prevent="copyRobokassaResultUrl"
              >
                {{ $t('action.copy') }}
                <Copied ref="robokassaResultUrlCopied" />
              </a>
            </template>
            <span v-else>—</span>
          </div>
        </div>
        <div class="admin-settings__item">
          <div class="admin-settings__label">
            <div class="admin-settings__name">
              {{ $t('billing.admin.robokassaTestConnection') }}
            </div>
          </div>
          <div class="admin-settings__control">
            <Button
              size="small"
              type="secondary"
              :loading="robokassaTesting"
              @click="testRobokassaConnection"
            >
              {{ $t('billing.admin.robokassaTestConnection') }}
            </Button>
            <div
              v-if="robokassaTestResult"
              style="margin-top: 12px; font-size: 13px; line-height: 1.45"
              :style="{
                color: robokassaTestResult.ok
                  ? 'var(--color-success-600)'
                  : 'var(--color-error-600)',
              }"
            >
              <div>{{ robokassaTestResult.message }}</div>
              <ul
                v-if="robokassaTestResult.checks?.length"
                style="margin: 8px 0 0; padding-left: 18px"
              >
                <li
                  v-for="(check, idx) in robokassaTestResult.checks"
                  :key="idx"
                >
                  {{ check.ok ? '✓' : '✗' }} {{ check.name }}:
                  {{ check.detail }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- YooKassa -->
      <div class="admin-settings__group">
        <h2 class="admin-settings__group-title">ЮKassa</h2>
        <div class="admin-settings__item">
          <div class="admin-settings__label">
            <div class="admin-settings__name">
              {{ $t('billing.admin.status') }}
            </div>
          </div>
          <div class="admin-settings__control">
            <SwitchInput
              :value="isYookassaActive"
              @input="toggleProvider('yookassa', $event)"
            >
              {{
                isYookassaActive
                  ? $t('billing.admin.active')
                  : $t('billing.admin.inactive')
              }}
            </SwitchInput>
          </div>
        </div>
        <div class="admin-settings__item">
          <div class="admin-settings__label">
            <div class="admin-settings__name">Shop ID</div>
          </div>
          <div class="admin-settings__control">
            <FormInput
              :value="yookassaConfig.shop_id"
              @input="yookassaConfig.shop_id = $event"
              @blur="saveProvider('yookassa')"
            />
          </div>
        </div>
        <div class="admin-settings__item">
          <div class="admin-settings__label">
            <div class="admin-settings__name">Secret Key</div>
            <div class="admin-settings__description">
              {{ $t('billing.admin.robokassaPasswordHint') }}
            </div>
          </div>
          <div class="admin-settings__control">
            <FormInput
              :value="yookassaConfig.secret_key_input"
              @focus="onPasswordFocus('yookassa', 'secret_key')"
              @input="yookassaConfig.secret_key_input = $event"
              @blur="saveProviderPassword('yookassa', 'secret_key')"
            />
          </div>
        </div>
        <div class="admin-settings__item">
          <div class="admin-settings__label">
            <div class="admin-settings__name">
              {{ $t('billing.admin.testMode') }}
            </div>
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
  </div>
</template>

<script setup>
import { reactive, computed, onMounted, ref } from 'vue'
import { useNuxtApp } from '#app'
import { useStore } from 'vuex'
import { notifyIf } from '@baserow/modules/core/utils/error'
import BillingService from '@baserow/modules/billing/services/billing'
import { copyToClipboard } from '@baserow/modules/database/utils/clipboard'

definePageMeta({
  layout: 'app',
  middleware: 'staff',
})

const { $client, $i18n } = useNuxtApp()
useHead({ title: $i18n.t('billing.admin.paymentProviders') })

const store = useStore()
const app = { $client }

const robokassaHashOptions = [
  { value: 'md5', name: 'MD5' },
  { value: 'sha1', name: 'SHA1' },
  { value: 'sha256', name: 'SHA256' },
  { value: 'sha384', name: 'SHA384' },
  { value: 'sha512', name: 'SHA512' },
]

const robokassaConfig = reactive({
  merchant_login: '',
  password1_input: '',
  password1_mask: '',
  password2_input: '',
  password2_mask: '',
  test_mode: true,
  hash_algorithm: 'md5',
  fiscalization_enabled: false,
})

const yookassaConfig = reactive({
  shop_id: '',
  secret_key_input: '',
  secret_key_mask: '',
  test_mode: true,
})

const robokassaResultUrl = ref('')
const robokassaResultUrlCopied = ref(null)
const robokassaTesting = ref(false)
const robokassaTestResult = ref(null)

const adminProviders = computed(() => store.getters['billing/getAdminProviders'])

const isRobokassaActive = computed(() => {
  const p = adminProviders.value.find((pr) => pr.provider_type === 'robokassa')
  return p?.is_active || false
})
const isYookassaActive = computed(() => {
  const p = adminProviders.value.find((pr) => pr.provider_type === 'yookassa')
  return p?.is_active || false
})

function syncProviderConfigs() {
  const robo = adminProviders.value.find(
    (p) => p.provider_type === 'robokassa'
  )
  if (robo) {
    robokassaConfig.merchant_login = robo.merchant_login || ''
    robokassaConfig.test_mode = robo.test_mode ?? true
    robokassaConfig.hash_algorithm = robo.hash_algorithm || 'md5'
    robokassaConfig.fiscalization_enabled = robo.fiscalization_enabled ?? false
    robokassaConfig.password1_mask = robo.password1 || ''
    robokassaConfig.password2_mask = robo.password2 || ''
    robokassaConfig.password1_input = robokassaConfig.password1_mask
    robokassaConfig.password2_input = robokassaConfig.password2_mask
  }
  const yoo = adminProviders.value.find(
    (p) => p.provider_type === 'yookassa'
  )
  if (yoo) {
    yookassaConfig.shop_id = yoo.shop_id || ''
    yookassaConfig.test_mode = yoo.test_mode ?? true
    yookassaConfig.secret_key_mask = yoo.secret_key || ''
    yookassaConfig.secret_key_input = yookassaConfig.secret_key_mask
  }
}

onMounted(async () => {
  try {
    await store.dispatch('billing/adminFetchProviders', { app })
    syncProviderConfigs()
  } catch (e) {
    notifyIf(e)
  }
  try {
    const { data } = await BillingService($client).adminGetRobokassaUrls()
    robokassaResultUrl.value = data.robokassa_result_url || ''
  } catch (e) {
    notifyIf(e)
  }
})

function copyRobokassaResultUrl() {
  copyToClipboard(robokassaResultUrl.value)
  robokassaResultUrlCopied.value?.show()
}

function onPasswordFocus(type, field) {
  const cfg = type === 'robokassa' ? robokassaConfig : yookassaConfig
  const inputKey = `${field}_input`
  const maskKey = `${field}_mask`
  if (cfg[inputKey] && cfg[inputKey] === cfg[maskKey]) {
    cfg[inputKey] = ''
  }
}

async function toggleProvider(type, active) {
  try {
    if (active) {
      await store.dispatch('billing/adminActivateProvider', {
        app,
        providerType: type,
      })
    } else {
      await store.dispatch('billing/adminDeactivateProvider', {
        app,
        providerType: type,
      })
    }
    syncProviderConfigs()
  } catch (e) {
    notifyIf(e)
  }
}

async function saveProvider(type) {
  try {
    const data =
      type === 'robokassa'
        ? { merchant_login: robokassaConfig.merchant_login }
        : { shop_id: yookassaConfig.shop_id }
    await store.dispatch('billing/adminUpdateProvider', {
      app,
      providerType: type,
      providerData: data,
    })
    syncProviderConfigs()
  } catch (e) {
    notifyIf(e)
  }
}

async function saveProviderPassword(type, field) {
  const cfg = type === 'robokassa' ? robokassaConfig : yookassaConfig
  const inputField = cfg[`${field}_input`]
  const mask = cfg[`${field}_mask`]
  if (!inputField || inputField === mask) {
    // Restore mask display if user left the field empty / unchanged.
    cfg[`${field}_input`] = mask || ''
    return
  }
  try {
    await store.dispatch('billing/adminUpdateProvider', {
      app,
      providerType: type,
      providerData: { [field]: inputField },
    })
    await store.dispatch('billing/adminFetchProviders', { app })
    syncProviderConfigs()
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

async function testRobokassaConnection() {
  robokassaTesting.value = true
  robokassaTestResult.value = null
  try {
    const { data } = await BillingService($client).adminTestRobokassa()
    robokassaTestResult.value = data
    await store.dispatch('toast/success', {
      title: $i18n.t('billing.admin.robokassaTestConnectionOk'),
      message: data.message,
    })
  } catch (e) {
    const data = e?.response?.data || e?.handler?.response?.data
    if (data && typeof data === 'object' && 'ok' in data) {
      robokassaTestResult.value = data
      await store.dispatch('toast/error', {
        title: $i18n.t('billing.admin.robokassaTestConnectionFail'),
        message: data.message || '',
      })
    } else {
      notifyIf(e)
    }
  } finally {
    robokassaTesting.value = false
  }
}
</script>
