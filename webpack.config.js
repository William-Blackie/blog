const path = require("path");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
    mode: "production",
    entry: "./website/static_src/js/main.js",
    output: {
        filename: "[name].js",
        path: path.resolve(__dirname, './website/static_compiled'),
    },
    plugins: [new MiniCssExtractPlugin({
            filename: "[name].css",
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
    devtool: 'source-map',
    devServer: {
        // Enable gzip compression for everything served.
        compress: true,
        host: '0.0.0.0',
        port: 3000,
        proxy: {
            context: () => true,
            target: 'http://localhost:8000',
        },
        client: {
            logging: 'error',
            // Shows a full-screen overlay in the browser when there are compiler errors.
            overlay: true,
        },
        static: {
            directory: path.resolve(__dirname, 'static'),
        },
        devMiddleware: {
            // Write compiled files to disk. This makes live-reload work on both port 3000 and 8000.
            writeToDisk: true,
            index: '',
            publicPath: '/static/',
        },
    }
}