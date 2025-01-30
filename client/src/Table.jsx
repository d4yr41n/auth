import { useState, useEffect } from 'react'
import request from "./request"


export default function Table({ auth, setAuth }) {
  const [data, setData] = useState([])
  function exit() {
    localStorage.setItem("auth", null)
    setAuth(null)
  }

  useEffect(() => {
    request("/users", auth)
    .then(response => response.json())
    .then(data => setData(data))
  }, [])

  let keys = []
  if (data.length)
    keys = Object.keys(data[0])

  return <>
    <p>Users<button onClick={exit} className="float-right">Exit</button></p>
    <table>
      <thead>
        <tr>
          {keys.map(i => <th key={i}>{i}</th>)}
        </tr>
      </thead>
      <tbody>
        {data.map((i, index) =>
          <tr key={index}>
            {keys.map(j => <td key={j}>{i[j]}</td>)}
          </tr>
        )}
      </tbody>
    </table>
  </>
}
