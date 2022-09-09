const path = require("path");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
    mode: "production",
    entry: "./website/static_src/js/main.js",
    output: {
        filename: "main.js",
        path: path.resolve(__dirname, './website/static_compiled')
    },
    plugins: [new MiniCssExtractPlugin({
            filename: "main.css",
        }),
        new CopyPlugin({
            patterns: [{
                from: "website/static_src/favicons/",
                to: "favicons/"
            }],
        }),
    ],
    module: {
        rules: [{
            test: /\.css$/,
            use: [
                MiniCssExtractPlugin.loader,
                "css-loader",
                "postcss-loader"
            ]
        }]
    },
    devServer: {
        static: path.join(__dirname, './website/static_compiled'), // boolean | string | array | object, static file location
        devMiddleware: {
            index: true,
            mimeTypes: { phtml: 'text/html' },
            publicPath: '/publicPathForDevServe',
            serverSideRender: true,
            writeToDisk: true,
        },
        hot: true, // hot module replacement. Depends on HotModuleReplacementPlugin
        liveReload: true,
    },
}