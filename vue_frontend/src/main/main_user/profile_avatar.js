import { createApp } from 'vue'
import App from './../../views/User/ProfileAvatar.vue'
import router from './../../router'
import * as sabitler from "./../../sabitler.js"


import axios from 'axios'
import VueAxios from 'vue-axios'
import Cookies from "js-cookie";




import * as i18nsabitler from './../../i18n.js';



axios.defaults.baseURL = sabitler.apiBaseURL;
axios.defaults.headers = {
    "Content-Type": "application/json",
    "X-CSRFToken": Cookies.get("csrftoken"),
}


import Toast from "vue-toastification";
// Import the CSS or use your own!
import "vue-toastification/dist/index.css";

const options = {
    // You can set your default options herey
    timeout: 3000
};



createApp(App).use(router).use(VueAxios, axios).use(i18nsabitler.GetLangJs()).use(Toast, options).mount('#app')