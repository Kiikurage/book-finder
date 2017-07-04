const { CheckerPlugin } = require('awesome-typescript-loader');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const HTMLWebpackPlugin = require('html-webpack-plugin');

const path = require('path');

module.exports = {
	entry: {
		'index': './src/scripts/index/index.tsx',
	},
	output: {
		path: path.resolve(__dirname, './build'),
		filename: '[name].js'
	},
	module: {
		rules: [{
			test: /\.tsx?$/,
			use: [{
				loader: 'awesome-typescript-loader'
			}]
		}, {
			test: /\.scss?$/,
			use: ExtractTextPlugin.extract({
				fallback: 'style-loader',
				use: ['css-loader', 'postcss-loader', 'sass-loader']
			})
		}]
	},
	resolve: {
		modules: [
			path.join(__dirname, './node_modules'),
		],
		extensions: ['.ts', '.tsx', '.js', '.jsx', '.scss']
	},
	plugins: [
		new ExtractTextPlugin({
			filename: getPath => getPath('[name].css'),
			allChunks: true
		}),
		new CheckerPlugin(),
		new HTMLWebpackPlugin({
			filename: 'index.html',
			inject: 'head',
			template: './src/html/index.html',
			chunks: ['index'],
			inlineSource: '.(css)$',
			minify: null
		}),
		new CopyWebpackPlugin([{
			from: './src/static',
			to: './'
		}]),
	]
};