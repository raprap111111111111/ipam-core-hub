import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./layouts/Main.css";

createApp(App).use(router).mount("#app");