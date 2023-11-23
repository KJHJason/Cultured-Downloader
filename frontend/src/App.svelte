<!-- <script>
  import logo from './assets/images/logo-universal.png'
  import {Greet, GetName} from '../wailsjs/go/main/App.js'

  let resultText = "Please enter your name below 👇"
  let name

  GetName().then(result => name = result)

  function greet() {
    Greet(name).then(result => resultText = result)
  }
</script>

<main>
  <img alt="Wails logo" id="logo" src="{logo}">
  <div class="result" id="result">{resultText}</div>
  <div class="input-box" id="input">
    <input autocomplete="off" bind:value={name} class="input" id="name" type="text"/>
    <button class="btn" on:click={greet}>Greet</button>
  </div>

  <div id="input" class="mb-4" data-wails-no-drag>
    <label class="block text-sm font-bold mb-2" for="name">
      Name
    </label>
    <input id="name" type="text" bind:value={name} class="shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" on:click={greet}>Greetings</button>
  </div>
</main> -->