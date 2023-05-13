const { defineConfig } = require('@vue/cli-service')

const BundleTracker = require("webpack-bundle-tracker");

const pages = {
    main: {
        entry: "./src/main/main_home/main.js",
        chunks: ["chunk-vendors"],
    },
    user_profile_avatar: {
        entry: "./src/main/main_user/profile_avatar.js",
        chunks: ["chunk-vendors"],
    }
};

module.exports = defineConfig({
    transpileDependencies: true,
})


module.exports = {
    pages: pages,
    filenameHashing: true,
    productionSourceMap: false,
    publicPath: process.env.NODE_ENV === "production" ?
        "https://aslkpl.s3.eu-central-1.amazonaws.com/static/vue" : "http://localhost:8093/",
    outputDir: "../static/vue/",

    chainWebpack: (config) => {
        config.optimization.splitChunks({
            cacheGroups: {
                vendor: {
                    test: /[\\/]node_modules[\\/]/,
                    name: "chunk-vendors",
                    chunks: "all",
                    priority: 1,
                },
            },
        });

        Object.keys(pages).forEach((page) => {
            config.plugins.delete(`html-${page}`);
            config.plugins.delete(`preload-${page}`);
            config.plugins.delete(`prefetch-${page}`);
        });

        config
            .plugin("BundleTracker")
            .use(BundleTracker, [{ filename: "../vue_frontend/webpack-stats.json" }]);

        config.resolve.alias.set("__STATIC__", "static");

        config.devServer
            //.public("http://localhost:8093")
            .host("localhost")
            .port(8093)
            //.hotOnly(true)
            //.watchOptions({ poll: 1000 })
            .https(false)
            .headers({ "Access-Control-Allow-Origin": ["*"] });

        // config.performance
        //     .maxEntrypointSize(900000)
        //     .maxAssetSize(900000)
    },
};