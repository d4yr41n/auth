import { useEffect } from 'react'

export default function Auth({ setAuth }) {
  function auth(formData) {
    const username = formData.get("username")
    const password = formData.get("password")
    const type = formData.get("type")
    fetch("http://localhost:8000/" + type, {
      method: "POST",
      body: JSON.stringify({
        username: username,
        password: password
      })
    }).then(response => {
      let auth
      if (response.status == 200) {
        auth = btoa(username + ':' + password)
        localStorage.setItem("auth", auth)
        setAuth(auth)
      }
    })
  }

  return <form action={auth}>
    <label>Username <input name="username" required/></label>
    <label>Password <input name="password"/></label>
    <div className="buttons">
      <button name="type" value="register" type="submit">Register</button>
      <button name="type" value="login" type="submit">Log In</button>
    </div>
  </form>
}
