<template>
  <div class="layout__col-2-scroll layout__col-2-scroll--white-background">
    <div style="max-width: 1100px; margin: 0 auto; padding: 32px 24px">
      <!-- Current subscription -->
      <div
        v-if="subscription"
        style="
          margin-bottom: 32px;
          padding: 20px 24px;
          border-radius: 8px;
          background: var(--color-primary-100);
          border: 1px solid var(--color-primary-200);
        "
      >
        <div style="display: flex; align-items: center; gap: 12px">
          <i
            class="iconoir-credit-card"
            style="font-size: 24px; color: var(--color-primary-500)"
          ></i>
          <div>
            <div style="font-weight: 600; font-size: 16px">
              {{ $t('billing.user.yourPlan') }}:
              <span style="color: var(--color-primary-500)">
                {{ subscription.plan?.name || 'Free' }}
              </span>
            </div>
            <div
              v-if="subscription.status"
              style="font-size: 13px; color: var(--color-neutral-500)"
            >
              {{ $t('billing.user.status') }}: {{ subscription.status }}
              <template v-if="subscription.current_period_end">
                &middot;
                {{ $t('billing.user.until') }}
                {{ formatDate(subscription.current_period_end) }}
              </template>
            </div>
          </div>
          <div style="margin-left: auto">
            <Button
              v-if="
                subscription.plan &&
                subscription.plan.slug !== 'free' &&
                subscription.status !== 'cancelled'
              "
              type="secondary"
              size="small"
              :loading="cancelling"
              @click="cancelSub"
            >
              {{ $t('billing.user.cancelSubscription') }}
            </Button>
          </div>
        </div>
      </div>

      <!-- Plans -->
      <h1 style="margin-bottom: 8px">{{ $t('billing.user.choosePlan') }}</h1>
      <p style="color: var(--color-neutral-500); margin-bottom: 24px">
        {{ $t('billing.user.choosePlanDescription') }}
      </p>

      <!-- Billing period toggle -->
      <div
        style="
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 24px;
        "
      >
        <span
          :style="{
            fontWeight: billingPeriod === 'monthly' ? '600' : '400',
            cursor: 'pointer',
          }"
          @click="billingPeriod = 'monthly'"
        >
          {{ $t('billing.user.monthly') }}
        </span>
        <SwitchInput
          :value="billingPeriod === 'yearly'"
          @input="billingPeriod = $event ? 'yearly' : 'monthly'"
        />
        <span
          :style="{
            fontWeight: billingPeriod === 'yearly' ? '600' : '400',
            cursor: 'pointer',
          }"
          @click="billingPeriod = 'yearly'"
        >
          {{ $t('billing.user.yearly') }}
          <Badge v-if="hasYearlyDiscount" color="green" bold>
            {{ $t('billing.user.save') }}
          </Badge>
        </span>
      </div>

      <!-- Plan cards -->
      <div v-if="loading" class="loading" style="margin: 40px 0"></div>
      <div
        v-else
        style="display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px"
      >
        <div
          v-for="plan in plans"
          :key="plan.id"
          style="
            border: 2px solid var(--color-neutral-200);
            border-radius: 10px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            transition: border-color 0.15s;
          "
          :style="{
            borderColor: isCurrentPlan(plan)
              ? 'var(--color-primary-500)'
              : 'var(--color-neutral-200)',
          }"
        >
          <div
            style="
              font-size: 18px;
              font-weight: 700;
              margin-bottom: 4px;
            "
          >
            {{ plan.name }}
          </div>
          <div
            v-if="plan.description"
            style="
              font-size: 13px;
              color: var(--color-neutral-500);
              margin-bottom: 16px;
            "
          >
            {{ plan.description }}
          </div>

          <!-- Price -->
          <div style="margin-bottom: 16px">
            <span style="font-size: 32px; font-weight: 700">
              {{ displayPrice(plan) }}
            </span>
            <span
              v-if="displayPrice(plan) !== '0'"
              style="font-size: 14px; color: var(--color-neutral-500)"
            >
              {{ plan.currency }} /
              {{
                billingPeriod === 'yearly'
                  ? $t('billing.user.year')
                  : $t('billing.user.month')
              }}
            </span>
            <span
              v-else
              style="font-size: 14px; color: var(--color-neutral-500)"
            >
              {{ $t('billing.user.free') }}
            </span>
          </div>

          <div style="flex: 1; margin-bottom: 20px">
            <!-- Limits -->
            <ul
              class="billing-plan-list"
              style="list-style: none; padding: 0; margin: 0"
            >
              <li
                v-for="(limit, idx) in planLimitLines(plan)"
                :key="'lim-' + idx"
                class="billing-plan-list__item"
              >
                <i
                  class="iconoir-check billing-plan-list__icon"
                  style="color: var(--color-success-600); font-size: 14px"
                ></i>
                {{ limit }}
              </li>
            </ul>

            <!-- Features (each on its own row) -->
            <template v-if="plan.features && plan.features.length">
              <div
                style="
                  font-size: 11px;
                  font-weight: 600;
                  text-transform: uppercase;
                  letter-spacing: 0.04em;
                  color: var(--color-neutral-500);
                  margin: 12px 0 6px;
                "
              >
                {{ $t('billing.user.includedFeatures') }}
              </div>
              <ul class="billing-plan-list" style="list-style: none; padding: 0; margin: 0">
                <li
                  v-for="feat in plan.features"
                  :key="'feat-' + feat"
                  class="billing-plan-list__item"
                >
                  <i
                    class="iconoir-check billing-plan-list__icon"
                    style="color: var(--color-success-600); font-size: 14px"
                  ></i>
                  {{ featureLabel(feat) }}
                </li>
              </ul>
            </template>
          </div>

          <!-- Action button -->
          <Button
            v-if="isCurrentPlan(plan)"
            type="secondary"
            :disabled="true"
            full-width
          >
            {{ $t('billing.user.currentPlan') }}
          </Button>
          <Button
            v-else
            :loading="subscribingPlanId === plan.id"
            :disabled="subscribingPlanId !== null"
            full-width
            @click="subscribeToPlan(plan)"
          >
            {{
              isFree(plan)
                ? $t('billing.user.switchToFree')
                : $t('billing.user.subscribe')
            }}
          </Button>
        </div>
      </div>

      <!-- Payment history -->
      <div v-if="payments.length > 0" style="margin-top: 48px">
        <h2 style="margin-bottom: 16px">
          {{ $t('billing.user.paymentHistory') }}
        </h2>
        <table style="width: 100%; border-collapse: collapse">
          <thead>
            <tr
              style="
                text-align: left;
                border-bottom: 2px solid var(--color-neutral-200);
              "
            >
              <th style="padding: 8px">{{ $t('billing.user.date') }}</th>
              <th style="padding: 8px">{{ $t('billing.user.description') }}</th>
              <th style="padding: 8px">{{ $t('billing.user.amount') }}</th>
              <th style="padding: 8px">{{ $t('billing.user.paymentStatus') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="payment in payments"
              :key="payment.id"
              style="border-bottom: 1px solid var(--color-neutral-100)"
            >
              <td style="padding: 8px">{{ formatDate(payment.created_at) }}</td>
              <td style="padding: 8px">{{ payment.description }}</td>
              <td style="padding: 8px">
                {{ payment.amount }} {{ payment.currency }}
              </td>
              <td style="padding: 8px">
                <Badge
                  :color="payment.status === 'succeeded' ? 'green' : 'neutral'"
                  bold
                >
                  {{ payment.status }}
                </Badge>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useNuxtApp } from '#app'
import { useStore } from 'vuex'
import { notifyIf } from '@baserow/modules/core/utils/error'

definePageMeta({
  layout: 'app',
  middleware: 'authenticated',
})

const { $client, $i18n } = useNuxtApp()
const { t: $t, te } = useI18n()
useHead({ title: $i18n.t('billing.user.title') })

const store = useStore()
const app = { $client }

const loading = ref(true)
const billingPeriod = ref('monthly')
const subscribingPlanId = ref(null)
const cancelling = ref(false)

const plans = computed(() => store.getters['billing/getPlans'])
const subscription = computed(() => store.getters['billing/getSubscription'])
const payments = computed(() => store.getters['billing/getPayments'])

const hasYearlyDiscount = computed(() => {
  return plans.value.some(
    (p) =>
      p.price_yearly > 0 &&
      p.price_monthly > 0 &&
      p.price_yearly < p.price_monthly * 12
  )
})

onMounted(async () => {
  try {
    await Promise.all([
      store.dispatch('billing/fetchPlans', { app }),
      store.dispatch('billing/fetchSubscription', { app }),
      store.dispatch('billing/fetchPayments', { app }),
    ])
  } catch (e) {
    notifyIf(e)
  }
  loading.value = false
})

function isCurrentPlan(plan) {
  return subscription.value?.plan?.id === plan.id
}

function isFree(plan) {
  return plan.price_monthly == 0 && plan.price_yearly == 0
}

function displayPrice(plan) {
  const price =
    billingPeriod.value === 'yearly' ? plan.price_yearly : plan.price_monthly
  return parseFloat(price) === 0 ? '0' : parseFloat(price).toLocaleString()
}

function planLimitLines(plan) {
  const lines = []
  const inf = $t('billing.user.unlimitedShort')

  const hasValue = (v) =>
    v !== null && v !== undefined && v !== '' && Number(v) > 0

  lines.push(
    hasValue(plan.max_rows_per_workspace)
      ? `${plan.max_rows_per_workspace} ${$t('billing.user.limitRows')}`
      : `${inf} ${$t('billing.user.limitRows')}`
  )
  lines.push(
    hasValue(plan.max_storage_mb)
      ? `${plan.max_storage_mb} MB ${$t('billing.user.limitStorage')}`
      : `${inf} ${$t('billing.user.limitStorage')}`
  )
  lines.push(
    hasValue(plan.max_workspaces)
      ? `${plan.max_workspaces} ${$t('billing.user.limitWorkspaces')}`
      : `${inf} ${$t('billing.user.limitWorkspaces')}`
  )
  lines.push(
    hasValue(plan.max_collaborators_per_workspace)
      ? `${plan.max_collaborators_per_workspace} ${$t('billing.user.limitCollaborators')}`
      : `${inf} ${$t('billing.user.limitCollaborators')}`
  )
  if (hasValue(plan.max_automations)) {
    lines.push(
      `${plan.max_automations} ${$t('billing.user.limitAutomations')}`
    )
  }
  if (hasValue(plan.max_api_calls_per_month)) {
    lines.push(
      `${plan.max_api_calls_per_month} ${$t('billing.user.limitApiCalls')}`
    )
  }
  if (hasValue(plan.max_file_upload_size_mb)) {
    lines.push(
      `${plan.max_file_upload_size_mb} MB ${$t('billing.user.limitPerFile')}`
    )
  }
  return lines
}

function featureLabel(key) {
  const path = `billing.featureLabels.${key}`
  if (te(path)) {
    return $t(path)
  }
  return String(key).replace(/_/g, ' ')
}

function formatDate(date) {
  if (!date) return ''
  return new Date(date).toLocaleDateString()
}

async function subscribeToPlan(plan) {
  subscribingPlanId.value = plan.id
  try {
    const result = await store.dispatch('billing/subscribe', {
      app,
      planId: plan.id,
      billingPeriod: billingPeriod.value,
    })

    if (result.payment_url) {
      window.location.href = result.payment_url
      return
    }

    await store.dispatch('billing/fetchSubscription', { app })
  } catch (e) {
    notifyIf(e)
  }
  subscribingPlanId.value = null
}

async function cancelSub() {
  cancelling.value = true
  try {
    await store.dispatch('billing/cancelSubscription', { app })
  } catch (e) {
    notifyIf(e)
  }
  cancelling.value = false
}
</script>

<style scoped>
.billing-plan-list__item {
  padding: 4px 0;
  font-size: 13px;
  display: flex;
  align-items: flex-start;
  gap: 6px;
  line-height: 1.35;
}

.billing-plan-list__icon {
  flex-shrink: 0;
  margin-top: 2px;
}
</style>
