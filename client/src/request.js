export default function request(path, auth) {
  const headers = {}
  if (auth)
    headers["Authorization"] = "Basic " + auth

  return fetch("http://localhost:8000" + path,  {
    headers: headers
  })
}
