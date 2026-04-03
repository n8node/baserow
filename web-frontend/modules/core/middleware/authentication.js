import {
  getTokenIfEnoughTimeLeft,
  setToken,
  setUserSessionCookie,
} from '@baserow/modules/core/utils/auth'

/**
 * Public homepage (`/`) shows the marketing landing for guests. A stale jwt cookie
 * would make `auth/refresh` return 401; we must not send users to /login in that case
 * (tokens are already cleared inside `refresh`).
 *
 * Route `name` can differ in production (i18n / Nuxt); use meta + path as fallbacks.
 */
function isPublicLandingHome(to) {
  if (to.meta.publicGuestHome === true) {
    return true
  }
  if (to.name === 'index') {
    return true
  }
  if (typeof to.name === 'string' && /^index($|___)/.test(to.name)) {
    return true
  }
  const path = (to.path || '/').replace(/\/+$/, '') || '/'
  return path === '/' || path === ''
}

export default defineNuxtRouteMiddleware(async (to) => {
  const nuxtApp = useNuxtApp()
  const store = nuxtApp.$store
  const event = import.meta.server ? useRequestEvent() : null

  // If nuxt generate or already authenticated, pass this middleware
  if ((import.meta.server && !event) || store.getters['auth/isAuthenticated']) {
    return
  }

  const userSession = to.query.user_session
  if (userSession) {
    await setUserSessionCookie(nuxtApp, userSession)
  }

  // token can be in the query string (SSO) or in the cookies (previous session)
  let refreshToken = to.query.token
  if (refreshToken) {
    await setToken(nuxtApp, refreshToken)
  } else {
    refreshToken = await getTokenIfEnoughTimeLeft(nuxtApp)
  }

  if (refreshToken) {
    try {
      await store.dispatch('auth/refresh', refreshToken)
    } catch (error) {
      if (error.response?.status === 401) {
        if (isPublicLandingHome(to)) {
          return
        }
        return navigateTo({ name: 'login' }, { external: true }) // force browser 302 redirect to get rid of the jwt cookie in the request headers
      }
    }
  }
})
