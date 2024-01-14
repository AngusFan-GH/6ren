const { VueLoaderPlugin } = require('vue-loader');
const CopyPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    mode: 'development',
    entry: {
        popup: './src/popup/popup.ts',
        background: './src/background.ts'
    },
    output: {
        path: __dirname + '/dist',
        filename: '[name].js'
    },
    resolve: {
        extensions: ['.ts', '.js', '.vue', '.json'],
        alias: {
            'vue$': 'vue/dist/vue.esm-bundler.js'
        }
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.ts$/,
                loader: 'ts-loader',
                options: { appendTsSuffixTo: [/\.vue$/] }
            },
            {
                test: /\.scss$/,
                use: [
                    'vue-style-loader',
                    'css-loader',
                    'sass-loader'
                ]
            },
            {
                test: /\.sass$/,
                use: [
                    'vue-style-loader',
                    'css-loader',
                    'sass-loader?indentedSyntax'
                ]
            },
            {
                test: /\.css$/,
                use: [
                    'vue-style-loader',
                    'css-loader'
                ]
            }
        ]
    },
    plugins: [
        new VueLoaderPlugin(),
        new HtmlWebpackPlugin({
            filename: 'popup.html', // 输出文件名
            template: 'src/popup/popup.html', // 模板文件路径
            chunks: ['popup'] // 指定包含的 chunk，与入口文件名称相对应
        }),
        new CopyPlugin({
            patterns: [
                { from: 'src/icons', to: 'icons' },
                { from: 'src/manifest.json', to: 'manifest.json' },
            ],
        })
    ]
};
