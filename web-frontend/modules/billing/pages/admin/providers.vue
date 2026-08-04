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
          </div>
          <div class="admin-settings__control">
            <FormInput
              :value="robokassaConfig.password1_input"
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
              :value="robokassaConfig.password2_input"
              type="password"
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
          </div>
          <div class="admin-settings__control">
            <FormInput
              :value="yookassaConfig.secret_key_input"
              type="password"
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
  password2_input: '',
  test_mode: true,
  hash_algorithm: 'md5',
  fiscalization_enabled: false,
})

const yookassaConfig = reactive({
  shop_id: '',
  secret_key_input: '',
  test_mode: true,
})

const robokassaResultUrl = ref('')
const robokassaResultUrlCopied = ref(null)

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
  }
  const yoo = adminProviders.value.find(
    (p) => p.provider_type === 'yookassa'
  )
  if (yoo) {
    yookassaConfig.shop_id = yoo.shop_id || ''
    yookassaConfig.test_mode = yoo.test_mode ?? true
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
  } catch (e) {
    notifyIf(e)
  }
}

async function saveProviderPassword(type, field) {
  const inputField =
    type === 'robokassa'
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
</script>
