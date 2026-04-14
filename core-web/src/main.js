// main.js
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./layouts/Main.css";
import Toast from "vue-toastification";

// Import the CSS directly from the node_modules path to bypass the alias
import "../node_modules/vue-toastification/dist/index.css"; 

const app = createApp(App);
app.use(router);
app.use(Toast);
app.mount("#app");