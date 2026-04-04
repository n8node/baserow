export default (client) => {
  return {
    getPlans() {
      return client.get('/billing/plans/')
    },
    getSubscription() {
      return client.get('/billing/subscription/')
    },
    subscribe(planId, billingPeriod = 'monthly') {
      return client.post('/billing/subscribe/', {
        plan_id: planId,
        billing_period: billingPeriod,
      })
    },
    cancelSubscription() {
      return client.post('/billing/cancel/')
    },
    getPayments() {
      return client.get('/billing/payments/')
    },

    // Admin endpoints
    adminGetPlans() {
      return client.get('/billing/admin/plans/')
    },
    adminCreatePlan(data) {
      return client.post('/billing/admin/plans/', data)
    },
    adminUpdatePlan(planId, data) {
      return client.patch(`/billing/admin/plans/${planId}/`, data)
    },
    adminDeletePlan(planId) {
      return client.delete(`/billing/admin/plans/${planId}/`)
    },
    adminSetDefaultPlan(planId) {
      return client.post(`/billing/admin/plans/${planId}/set-default/`)
    },
    adminGetRobokassaUrls() {
      return client.get('/billing/admin/robokassa-urls/')
    },
    adminGetProviders() {
      return client.get('/billing/admin/providers/')
    },
    adminUpdateProvider(providerType, data) {
      return client.patch(`/billing/admin/providers/${providerType}/`, data)
    },
    adminActivateProvider(providerType) {
      return client.post(
        `/billing/admin/providers/${providerType}/activate/`
      )
    },
    adminDeactivateProvider(providerType) {
      return client.post(
        `/billing/admin/providers/${providerType}/deactivate/`
      )
    },
    adminGetSubscriptions() {
      return client.get('/billing/admin/subscriptions/')
    },
    adminUpdateSubscription(subscriptionId, data) {
      return client.patch(
        `/billing/admin/subscriptions/${subscriptionId}/`,
        data
      )
    },
    adminGetAvailableFeatures() {
      return client.get('/billing/admin/available-features/')
    },
    adminAssignPlan(userId, planId) {
      return client.post('/billing/admin/assign-plan/', {
        user_id: userId,
        plan_id: planId,
      })
    },
  }
}
