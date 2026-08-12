var UglifyJS = require('uglify-js');
var CleanCSS = require('clean-css');
var fs = require('fs');
require('shelljs/global');
require('colors');

var fileConf = require('./files.conf.js')
var CSSJSfiles = fileConf.CSSJSfiles;

nowDate = new Date();
nowDateStr = nowDate.toISOString().slice(0, 10).replace(/-/g, "");

// remove preceding compressed files
rm('-rf', 'static/assets/*.min.js');
rm('-rf', 'static/assets/*.min.css');

cp('-f', 'node_modules/font-mfizz/dist/font-mfizz.eot', 'static/assets/');
cp('-f', 'node_modules/font-mfizz/dist/font-mfizz.svg', 'static/assets/');
cp('-f', 'node_modules/font-mfizz/dist/font-mfizz.ttf', 'static/assets/');
cp('-f', 'node_modules/font-mfizz/dist/font-mfizz.woff', 'static/assets/');

// Font Awesome 5's CSS references its webfonts as "../webfonts/..." relative to the
// compiled bundle at static/assets/app-*.min.css, i.e. static/webfonts/ on disk.
mkdir('-p', 'static/webfonts');
cp('-f', 'node_modules/components-font-awesome/webfonts/*', 'static/webfonts/');

// change link/src files to new file path
sed('-i', /(.*)[0-9]{8}(.*)/, '$1' + nowDateStr + '$2', '_includes/index_head.html');
sed('-i', /(.*)[0-9]{8}(.*)/, '$1' + nowDateStr + '$2', '_includes/head.html');
sed('-i', /(.*)[0-9]{8}(.*)/, '$1' + nowDateStr + '$2', '_includes/category.html');
sed('-i', /(.*)[0-9]{8}(.*)/, '$1' + nowDateStr + '$2', '404.html');


// compress js files function
function compressjs(pagename, filename, filelist) {
    console.log('Now compress ' + pagename + ' js files to ' + filename + ' ...')
    // uglify-js 3.x no longer reads files from disk itself; feed it {filename: source} instead.
    var sources = {};
    filelist.forEach(function(file) {
        sources[file] = fs.readFileSync(file, 'utf8');
    });
    var result = UglifyJS.minify(sources, {
        mangle: true,
        compress: {
            sequences: true,
            dead_code: true,
            conditionals: true,
            booleans: true,
            unused: true,
            if_return: true,
            join_vars: true,
            drop_console: true
        },
    });

    if (result.error) {
        throw result.error;
    }

    fs.writeFileSync('static/assets/' + filename, result.code);
    console.log(pagename.green + " js files compress succeed. You can find it at \"static/assets\".\n".green);
}

// compress css files function
function compresscss(pagename, filename, filelist) {
    console.log('Now compress ' + pagename + ' css files to ' + filename + ' ...')
    var result = new CleanCSS().minify(filelist);
    var output = new CleanCSS({
        level: {
            1: {
                transform: function(propertyName, propertyValue) {
                    if (propertyName == 'src' && propertyValue.indexOf('node_modules/bootstrap/dist/') > -1) {
                        return propertyValue.replace('node_modules/bootstrap/dist/', '');
                    }
                    if (propertyName == 'src' && propertyValue.indexOf('node_modules/components-font-awesome/') > -1) {
                        return propertyValue.replace('node_modules/components-font-awesome/', '');
                    }
                    if (propertyName == 'src' && propertyValue.indexOf('node_modules/font-mfizz/dist/') > -1) {
                        return propertyValue.replace('node_modules/font-mfizz/dist/', '');
                    }
                    if (propertyName == 'background' && propertyValue.indexOf('static/img/') > -1) {
                        return propertyValue.replace('static/', '');
                    }
                    if (propertyName == 'background-image' && propertyValue.indexOf('static/img/') > -1) {
                        return propertyValue.replace('static/', '');
                    }
                }
            }
        }
    }).minify(result.styles);

    fs.writeFileSync('static/assets/' + filename, output.styles);
    console.log(pagename.green + " css files compress succeed. You can find it at \"static/assets\".\n".green);
}

for (i = 0; i < CSSJSfiles.length; i++) {
    if (CSSJSfiles[i].type == 'css') {
        var filename = CSSJSfiles[i].prefix + nowDateStr + '.min.css'
        compresscss(CSSJSfiles[i].name, filename, CSSJSfiles[i].list)
    }
    if (CSSJSfiles[i].type == 'js') {
        var filename = CSSJSfiles[i].prefix + nowDateStr + '.min.js'
        compressjs(CSSJSfiles[i].name, filename, CSSJSfiles[i].list)
    }
}
