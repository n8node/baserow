import UserService from '@baserow/modules/core/services/admin/users'

function stripImpersonateUserQuery(query) {
  const nextQuery = { ...query }
  delete nextQuery['__impersonate-user']
  return nextQuery
}

function isAlreadyImpersonating(store) {
  try {
    return store.getters['impersonating/getImpersonating'] === true
  } catch {
    return false
  }
}

/**
 * We only want to allow impersonation when a page loads for the first time because
 * on first load several endpoints are called to fetch initial data like workspace,
 * applications, etc. Starting the impersonation when the page first loads, makes
 * sure that we never have to take this situation into account because it only
 * happens on first page load before everything is fetched.
 */
export default defineNuxtRouteMiddleware(async (to) => {
  if (!import.meta.server) return

  const nuxtApp = useNuxtApp()
  const store = nuxtApp.$store

  // If the query param is not provided, we don't want to do anything.
  if (!Object.prototype.hasOwnProperty.call(to.query, '__impersonate-user')) {
    return
  }

  const queryWithoutImpersonate = stripImpersonateUserQuery(to.query)

  // dashboardRedirect sends users to workspace with the same query string. If we
  // call the admin impersonate endpoint again here, the request uses the
  // impersonated user's JWT and the API correctly responds with 403.
  if (isAlreadyImpersonating(store)) {
    return navigateTo(
      { path: to.path, query: queryWithoutImpersonate, hash: to.hash },
      { replace: true }
    )
  }

  const userId = to.query['__impersonate-user']

  // Request the impersonate user data, this contains the `token` and `user` object.
  // This is needed to impersonate the user.
  const { data } = await UserService(nuxtApp.$client).impersonate(userId)

  // Override the existing user data based on the response of the impersonate endpoint.
  store.dispatch('auth/forceSetUserData', data)

  // Make sure that the auth doesn't override the JWT token cookie because we want
  // the admin one to persist.
  store.dispatch('auth/preventSetToken')

  // Set the impersonating state to true so that the warning in the top left corner
  // is visible.
  store.dispatch('impersonating/setImpersonating', true)

  return navigateTo(
    { path: to.path, query: queryWithoutImpersonate, hash: to.hash },
    { replace: true }
  )
})
