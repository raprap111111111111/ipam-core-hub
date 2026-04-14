import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./layouts/Main.css";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

const app = createApp(App);

app.use(router);
app.use(Toast); // This is the missing line!

app.mount("#app");