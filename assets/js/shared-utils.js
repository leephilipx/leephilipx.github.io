function fileExists(url) {
  return fetch(url, { method: "HEAD" }).then(res => res.ok)
}
