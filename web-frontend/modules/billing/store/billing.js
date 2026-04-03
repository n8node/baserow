export const state = () => ({
  plans: [],
  subscription: null,
  payments: [],
  adminPlans: [],
  adminProviders: [],
  adminSubscriptions: [],
  availableFeatures: [],
})

export const mutations = {
  SET_PLANS(state, plans) {
    state.plans = plans
  },
  SET_SUBSCRIPTION(state, subscription) {
    state.subscription = subscription
  },
  SET_PAYMENTS(state, payments) {
    state.payments = payments
  },
  SET_ADMIN_PLANS(state, plans) {
    state.adminPlans = plans
  },
  SET_ADMIN_PROVIDERS(state, providers) {
    state.adminProviders = providers
  },
  SET_ADMIN_SUBSCRIPTIONS(state, subscriptions) {
    state.adminSubscriptions = subscriptions
  },
  SET_AVAILABLE_FEATURES(state, features) {
    state.availableFeatures = features
  },
  UPDATE_ADMIN_PLAN(state, updatedPlan) {
    const idx = state.adminPlans.findIndex((p) => p.id === updatedPlan.id)
    if (idx !== -1) {
      state.adminPlans.splice(idx, 1, updatedPlan)
    }
  },
  ADD_ADMIN_PLAN(state, plan) {
    state.adminPlans.push(plan)
  },
  REMOVE_ADMIN_PLAN(state, planId) {
    state.adminPlans = state.adminPlans.filter((p) => p.id !== planId)
  },
  UPDATE_ADMIN_PROVIDER(state, provider) {
    const idx = state.adminProviders.findIndex(
      (p) => p.provider_type === provider.provider_type
    )
    if (idx !== -1) {
      state.adminProviders.splice(idx, 1, provider)
    } else {
      state.adminProviders.push(provider)
    }
  },
}

export const actions = {
  async fetchPlans({ commit }, { app }) {
    const BillingService = app.$client
      ? (await import('@baserow/modules/billing/services/billing')).default(
          app.$client
        )
      : null
    if (!BillingService) return
    const { data } = await BillingService.getPlans()
    commit('SET_PLANS', data)
  },

  async fetchSubscription({ commit }, { app }) {
    const BillingService = (
      await import('@baserow/modules/billing/services/billing')
    ).default(app.$client)
    const { data } = await BillingService.getSubscription()
    commit('SET_SUBSCRIPTION', data)
  },

  async fetchPayments({ commit }, { app }) {
    const BillingService = (
      await import('@baserow/modules/billing/services/billing')
    ).default(app.$client)
    const { data } = await BillingService.getPayments()
    commit('SET_PAYMENTS', data)
  },

  async subscribe(_, { app, planId, billingPeriod }) {
    const BillingService = (
      await import('@baserow/modules/billing/services/billing')
    ).default(app.$client)
    const { data } = await BillingService.subscribe(planId, billingPeriod)
    return data
  },

  async cancelSubscription({ commit }, { app }) {
    const BillingService = (
      await import('@baserow/modules/billing/services/billing')
    ).default(app.$client)
    const { data } = await BillingService.cancelSubscription()
    commit('SET_SUBSCRIPTION', data)
  },

  // Admin actions
  async adminFetchPlans({ commit }, { app }) {
    const BillingService = (
      await import('@baserow/modules/billing/services/billing')
    ).default(app.$client)
    const { data } = await BillingService.adminGetPlans()
    commit('SET_ADMIN_PLANS', data)
  },

  async adminCreatePlan({ commit }, { app, planData }) {
    const BillingService = (
      await import('@baserow/modules/billing/services/billing')
    ).default(app.$client)
    const { data } = await BillingService.adminCreatePlan(planData)
    commit('ADD_ADMIN_PLAN', data)
    return data
  },

  async adminUpdatePlan({ commit }, { app, planId, planData }) {
    const BillingService = (
      await import('@baserow/modules/billing/services/billing')
    ).default(app.$client)
    const { data } = await BillingService.adminUpdatePlan(planId, planData)
    commit('UPDATE_ADMIN_PLAN', data)
    return data
  },

  async adminDeletePlan({ commit }, { app, planId }) {
    const BillingService = (
      await import('@baserow/modules/billing/services/billing')
    ).default(app.$client)
    await BillingService.adminDeletePlan(planId)
    commit('REMOVE_ADMIN_PLAN', planId)
  },

  async adminSetDefaultPlan({ dispatch }, { app, planId }) {
    const BillingService = (
      await import('@baserow/modules/billing/services/billing')
    ).default(app.$client)
    await BillingService.adminSetDefaultPlan(planId)
    await dispatch('adminFetchPlans', { app })
  },

  async adminFetchProviders({ commit }, { app }) {
    const BillingService = (
      await import('@baserow/modules/billing/services/billing')
    ).default(app.$client)
    const { data } = await BillingService.adminGetProviders()
    commit('SET_ADMIN_PROVIDERS', data)
  },

  async adminUpdateProvider({ commit }, { app, providerType, providerData }) {
    const BillingService = (
      await import('@baserow/modules/billing/services/billing')
    ).default(app.$client)
    const { data } = await BillingService.adminUpdateProvider(
      providerType,
      providerData
    )
    commit('UPDATE_ADMIN_PROVIDER', data)
    return data
  },

  async adminActivateProvider({ dispatch }, { app, providerType }) {
    const BillingService = (
      await import('@baserow/modules/billing/services/billing')
    ).default(app.$client)
    await BillingService.adminActivateProvider(providerType)
    await dispatch('adminFetchProviders', { app })
  },

  async adminDeactivateProvider({ dispatch }, { app, providerType }) {
    const BillingService = (
      await import('@baserow/modules/billing/services/billing')
    ).default(app.$client)
    await BillingService.adminDeactivateProvider(providerType)
    await dispatch('adminFetchProviders', { app })
  },

  async adminFetchSubscriptions({ commit }, { app }) {
    const BillingService = (
      await import('@baserow/modules/billing/services/billing')
    ).default(app.$client)
    const { data } = await BillingService.adminGetSubscriptions()
    commit('SET_ADMIN_SUBSCRIPTIONS', data)
  },

  async adminFetchAvailableFeatures({ commit }, { app }) {
    const BillingService = (
      await import('@baserow/modules/billing/services/billing')
    ).default(app.$client)
    const { data } = await BillingService.adminGetAvailableFeatures()
    commit('SET_AVAILABLE_FEATURES', data)
  },
}

export const getters = {
  getPlans: (state) => state.plans,
  getSubscription: (state) => state.subscription,
  getPayments: (state) => state.payments,
  currentPlan: (state) => state.subscription?.plan || null,
  currentPlanSlug: (state) => state.subscription?.plan?.slug || 'free',
  getAdminPlans: (state) => state.adminPlans,
  getAdminProviders: (state) => state.adminProviders,
  getAdminSubscriptions: (state) => state.adminSubscriptions,
  getAvailableFeatures: (state) => state.availableFeatures,
  activeProvider: (state) =>
    state.adminProviders.find((p) => p.is_active) || null,
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
}
