import { useState } from 'react'
import appLogo from './assets/app_icon.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://github.com/Rualin/RDR" target="_blank">
          <img src={appLogo} className="logo" alt="App logo" />
        </a>
      </div>
      <h1>Medical documents recognition</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Test with new assets
        </p>
      </div>
      <p className="read-the-docs">
        v0.2
      </p>
    </>
  )
}

export default App
