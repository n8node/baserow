<template>
  <Modal ref="modal">
    <h2 class="box__title">
      {{ $t('billing.assignPlan.title', { username: user.username }) }}
    </h2>
    <Error :error="error"></Error>
    <div v-if="loading" class="loading"></div>
    <div v-else>
      <p class="margin-bottom-2">
        {{ $t('billing.assignPlan.currentPlan') }}:
        <strong>{{ user.billing_plan_name || '—' }}</strong>
      </p>
      <FormGroup :label="$t('billing.assignPlan.selectPlan')">
        <div class="dropdown" :class="{ 'dropdown--open': dropdownOpen }">
          <a class="dropdown__selected" @click="dropdownOpen = !dropdownOpen">
            <span class="dropdown__selected-text">
              {{ selectedPlanName || $t('billing.assignPlan.selectPlan') }}
            </span>
            <i class="dropdown__toggle-icon iconoir-nav-arrow-down"></i>
          </a>
          <div v-show="dropdownOpen" class="dropdown__items">
            <ul class="select__items">
              <li v-for="plan in plans" :key="plan.id">
                <a
                  class="select__item"
                  :class="{
                    'select__item--active': selectedPlanId === plan.id,
                  }"
                  @click="selectPlan(plan)"
                >
                  {{ plan.name }}
                  <span v-if="plan.is_default" style="opacity: 0.5">
                    ({{ $t('billing.assignPlan.default') }})
                  </span>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </FormGroup>
      <div
        style="
          margin-top: 16px;
          display: flex;
          gap: 8px;
          justify-content: flex-end;
        "
      >
        <Button type="secondary" @click="hide()">
          {{ $t('action.cancel') }}
        </Button>
        <Button :loading="saving" :disabled="!selectedPlanId" @click="assign">
          {{ $t('billing.assignPlan.assign') }}
        </Button>
      </div>
    </div>
  </Modal>
</template>

<script>
import modal from '@baserow/modules/core/mixins/modal'
import error from '@baserow/modules/core/mixins/error'

export default {
  name: 'AssignPlanModal',
  mixins: [modal, error],
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  emits: ['assigned'],
  data() {
    return {
      loading: false,
      saving: false,
      plans: [],
      selectedPlanId: null,
      dropdownOpen: false,
    }
  },
  computed: {
    selectedPlanName() {
      const plan = this.plans.find((p) => p.id === this.selectedPlanId)
      return plan ? plan.name : ''
    },
  },
  methods: {
    async show(...args) {
      modal.methods.show.call(this, ...args)
      this.selectedPlanId = this.user.billing_plan_id || null
      this.hideError()
      await this.fetchPlans()
    },
    async fetchPlans() {
      this.loading = true
      try {
        const BillingService = (
          await import('@baserow/modules/billing/services/billing')
        ).default(this.$client)
        const { data } = await BillingService.adminGetPlans()
        this.plans = data
      } catch (e) {
        this.handleError(e)
      }
      this.loading = false
    },
    selectPlan(plan) {
      this.selectedPlanId = plan.id
      this.dropdownOpen = false
    },
    async assign() {
      if (!this.selectedPlanId) return
      this.saving = true
      this.hideError()
      try {
        const BillingService = (
          await import('@baserow/modules/billing/services/billing')
        ).default(this.$client)
        const { data } = await BillingService.adminAssignPlan(
          this.user.id,
          this.selectedPlanId
        )
        const assignedPlan = this.plans.find(
          (p) => p.id === this.selectedPlanId
        )
        this.$emit('assigned', {
          userId: this.user.id,
          planId: this.selectedPlanId,
          planName: assignedPlan ? assignedPlan.name : data.plan_name,
          planSlug: assignedPlan ? assignedPlan.slug : '',
        })
        this.hide()
      } catch (e) {
        this.handleError(e)
      }
      this.saving = false
    },
  },
}
</script>
