import { useState, useEffect } from 'react'
import Auth from "./Auth"
import Table from "./Table"
import request from "./request"

export default function App() {
  const [code, setCode] = useState(0)
  const [auth, setAuth] = useState(localStorage.getItem("auth"))

  request("/auth", auth).then(response => setCode(response.status))

  return <>
    {!code ? <div className="center">loading...</div>
      : code == 200 ? <Table auth={auth} setAuth={setAuth}/>
      : <Auth setAuth={setAuth}/>}
  </>
}
