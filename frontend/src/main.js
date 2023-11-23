import "./style.css"
import "./tailwind.css"
import "./darkMode.js"
import "flowbite"
import App from "./App.svelte"
import Navbar from "./Navbar.svelte"

const app = new App({
  target: document.getElementById("app")
})
const navbar = new Navbar({
  target: document.getElementById("navbar")
})

export default app
export { navbar }
