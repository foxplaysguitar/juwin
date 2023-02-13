//Use jQuery in console

var jquery = document.createElement('script');
jquery.src = 'https://code.jquery.com/jquery-3.3.1.min.js';
document.getElementsByTagName('head')[0].appendChild(jquery);

/* －－－－－－－－－Pre-Check－－－－－－－－－ */

/* Check CSS/JS Files in Home */
var homeJsList = [];
var homeScriptArr = [];
document.querySelectorAll('script[src]').forEach(x => homeJsList.push(x.src))

/* Used in Home Page to check defer/async */
var scripts = document.querySelectorAll('script[src]');
var arr = [];
for (var i = 0; i < scripts.length; i++) {
    var att = scripts[i].attributes;
    if (!att.hasOwnProperty('async') && !att.hasOwnProperty('defer')) {
        arr.push(scripts[i].src)
    }
}
console.log(arr.join('\n\n'))

/* －－－－－－－－－Main Investigate－－－－－－－－－ */

var audit = {                       //if there's any problem, documented here.
    'h1': [],
    'h2': [],
    'h3': [],

    'no en': [],
    'no zh-TW': [],
    'no vi': [],
    'no th': [],
    'no id': [],
    'no zh-CN': [],

    'no og Title': [],
    'no og Desc': [],
    'no og Url': [],
    'no og SiteName': [],
    'no og Img': [],

    'haveBreadCrumb': false,
    'sameJs': true,


};

/* Gather All Pages （Without Canonical）*/                                  //Put In Home Page
var homePage = location.href;
var urls = [homePage];
var reg = new RegExp(homePage);
for (var i = 0; i < urls.length; i++) {
    fetch(urls[i]).then(res => res.text()).catch(err => { throw new Error('Fetch Failed ' + err) }).then(html => {
        var parser = new DOMParser();
        var doc = parser.parseFromString(html, 'text/html');
        doc.querySelectorAll('a[href]').forEach(x => {
            reg.test(x.href) ? urls.push(x.href) : ''
        });
        urls = Array.from(new Set(urls))
    })
}
setTimeout(() => { console.log(urls.join('\n')); }, 1000)

/* Gather All Pages （With Canonical）*/                                  //Put In Home Page   
var homePage = location.href;
var urls = [homePage];
var canonUrls = new Set();
var reg = new RegExp(homePage);
    fetch(urls[i]).then(res => res.text()).catch(err => { throw new Error('Fetch Failed ' + err) }).then(html => {
        var parser = new DOMParser();
        var doc = parser.parseFromString(html, 'text/html');
        var href = doc.querySelector('link[rel="canonical"]').href;
        canonUrls.add(href);
        doc.querySelectorAll('a[href]').forEach(x => {
            reg.test(x.href) ? urls.push(x.href) : ''
        });
        urls = Array.from(new Set(urls));
        return urls
    }).then(urls => {
        console.log(urls.join('\n'))
    })
    
setTimeout(() => {
    canonUrls = Array.from(canonUrls);
    console.log(canonUrls.join('\n'));
}, 1000)







/* －－－－－－－－－Others－－－－－－－－－ */


//Gather partners' links in partner page

var a = document.querySelectorAll('.product-inner a');
var arr = new Set();
for (var i = 0; i < a.length; i++) {
    arr.add(a[i].href)
}
arr = Array.from(arr);
console.log(arr.join('\n'))

