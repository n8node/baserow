/**
 * Generate ru.json from en.json (recursive string translation EN→RU).
 * Uses the public gtx endpoint (same as Google Translate widget). Run:
 *   node scripts/generate-ru-locales.mjs
 */
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const ROOT = path.join(__dirname, '..')

const cache = new Map()

/** Preserve vue-i18n {foo} and python %(name)s tokens while translating */
function shieldPlaceholders(s) {
  const parts = []
  let i = 0
  const re = /\{[^{}]+\}|%\([^)]+\)[sdif]|%[sdif]/g
  const out = s.replace(re, (m) => {
    parts.push(m)
    return `\uE000${i++}\uE001`
  })
  return { out, parts }
}

function unshieldPlaceholders(s, parts) {
  let r = s
  for (let j = 0; j < parts.length; j++) {
    r = r.replace(`\uE000${j}\uE001`, parts[j])
  }
  return r
}

function splitLong(s, max) {
  if (s.length <= max) return [s]
  const out = []
  let start = 0
  while (start < s.length) {
    let end = Math.min(start + max, s.length)
    if (end < s.length) {
      const sp = s.lastIndexOf(' ', end)
      if (sp > start) end = sp
    }
    const piece = s.slice(start, end).trimEnd()
    if (piece) out.push(piece)
    start = end
    while (start < s.length && s[start] === ' ') start++
  }
  return out.length ? out : [s]
}

async function translateLine(text) {
  if (!text.trim()) return text
  if (cache.has(text)) return cache.get(text)
  if (text.length > 1800) {
    const chunks = text.includes('\n')
      ? text.split('\n')
      : splitLong(text, 1500)
    const bits = []
    for (const c of chunks) {
      bits.push(c ? await translateLine(c) : '')
    }
    const out = text.includes('\n') ? bits.join('\n') : bits.join(' ')
    cache.set(text, out)
    return out
  }
  const { out: shielded, parts } = shieldPlaceholders(text)
  const url =
    'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ru&dt=t&q=' +
    encodeURIComponent(shielded)
  for (let attempt = 0; attempt < 5; attempt++) {
    try {
      const ac = new AbortController()
      const t = setTimeout(() => ac.abort(), 25000)
      const res = await fetch(url, {
        signal: ac.signal,
        headers: { 'User-Agent': 'Baserow-locale-script' },
      })
      clearTimeout(t)
      if (!res.ok) throw new Error(String(res.status))
      const data = await res.json()
      const raw = data[0].map((x) => x[0]).join('')
      const out = unshieldPlaceholders(raw, parts)
      cache.set(text, out)
      await new Promise((r) => setTimeout(r, 120))
      return out
    } catch (e) {
      console.warn('retry', attempt, e.message)
      await new Promise((r) => setTimeout(r, 800 * (attempt + 1)))
    }
  }
  console.warn('FAILED, keeping EN:', text.slice(0, 60))
  cache.set(text, text)
  return text
}

function collectStrings(obj, set) {
  if (obj === null || obj === undefined) return
  if (typeof obj === 'string') {
    if (obj.trim()) set.add(obj)
    return
  }
  if (Array.isArray(obj)) {
    obj.forEach((x) => collectStrings(x, set))
    return
  }
  if (typeof obj === 'object') {
    Object.values(obj).forEach((x) => collectStrings(x, set))
  }
}

function applyTranslations(obj) {
  if (obj === null || obj === undefined) return obj
  if (typeof obj === 'string') {
    if (!obj.trim()) return obj
    return cache.get(obj) ?? obj
  }
  if (Array.isArray(obj)) return obj.map((x) => applyTranslations(x))
  if (typeof obj === 'object') {
    const out = {}
    for (const [k, v] of Object.entries(obj)) out[k] = applyTranslations(v)
    return out
  }
  return obj
}

async function processEnJson(enPath) {
  const raw = fs.readFileSync(enPath, 'utf8')
  const data = JSON.parse(raw)
  const unique = new Set()
  collectStrings(data, unique)
  const list = [...unique].sort((a, b) => b.length - a.length)
  console.log(path.relative(ROOT, enPath), '→', list.length, 'unique strings')
  let i = 0
  for (const s of list) {
    i++
    if (i % 50 === 0) console.log(' ', i, '/', list.length)
    await translateLine(s)
  }
  const out = applyTranslations(data)
  const ruPath = path.join(path.dirname(enPath), 'ru.json')
  fs.writeFileSync(ruPath, JSON.stringify(out, null, 2) + '\n', 'utf8')
  console.log(' wrote', path.relative(ROOT, ruPath))
}

async function main() {
  const bases = [
    path.join(ROOT, 'web-frontend', 'modules'),
    path.join(ROOT, 'premium', 'web-frontend', 'modules'),
    path.join(ROOT, 'enterprise', 'web-frontend', 'modules'),
  ]
  const pending = []
  for (const base of bases) {
    if (!fs.existsSync(base)) continue
    ;(function walk(dir) {
      for (const name of fs.readdirSync(dir, { withFileTypes: true })) {
        const p = path.join(dir, name.name)
        if (name.isDirectory()) walk(p)
        else if (name.name === 'en.json' && p.includes(`${path.sep}locales${path.sep}`))
          pending.push(p)
      }
    })(base)
  }
  pending.sort()
  for (const enPath of pending) await processEnJson(enPath)
  console.log('Total cache size', cache.size)
}

main().catch((e) => {
  console.error(e)
  process.exit(1)
})
