import App from "./App.svelte";
import "./index.css";
import "flowbite";
import { mount } from "svelte";

const app = mount(App, {
    target: document.body,
});

export default app;
