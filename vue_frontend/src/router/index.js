import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";



const routes = [{
        path: "/:lang",
        name: "Home",
        component: Home,
    }

];

const router = createRouter({
    history: createWebHistory(), //process.env.BASE_URL bunu kaldırdım
    routes,
});

export default router;