var myLib = require('./myLib.js');
var fs = require('fs');
var system = require('system');
var page = require('webpage').create();

page.onConsoleMessage = function (msg) {
    // This suppresses Javascript errors from downloaded pages from printing
    //console.log(msg);
};

var cars = require('./car_list.js')
var hotels = require('./hotel_list.js')
var ecommerce = require('./ecommerce_list.js')

system.INITIAL_WAIT = 60 * 1000;
system.PAGE_LOAD_WAIT = 30 * 1000;
system.SEARCH_WAIT = 1 * 60 * 1000;
system.ERROR_RETRY_WAIT = 1 * 60 * 1000;
system.MAX_ERRORS = 2;

system.search_index = -1;
system.search_terms = [];
system.login = false;
system.clear_cookies = false;
system.persist_cookies = false;
system.result_dir = '.';
system.file_name_suffix = "";
system.username = "";
system.password = "";
system.errors = 0;

var service = false;
var store = false;
var store_list = false;
var store_map = false;

page.settings.userAgent = myLib.get_useragent('default');
page.customHeaders = {"Accept-Language":"en"};

system.args.forEach(function(arg, i) {
    parts = arg.split("=");
    if (parts[0] == '--store') {
      store = parts[1];
    }
    else if (parts[0] == '--service') {
        service = parts[1].toLowerCase();
    }
    else if (parts[0] == '--login') {
        s = parts[1].toLowerCase();
        if (s == 'true' || s == '1') system.login = true;
    }
    else if (parts[0] == '--username')
        system.username = parts[1];
    else if (parts[0] == '--password')
        system.password = parts[1];
    else if (parts[0] == '--clear-cookies')
        system.clear_cookies = 1;
    else if (parts[0] == '--referer')
        system.referer = parts[1];
    else if (parts[0] == '--persist-cookies') {
        system.persist_cookies = parts[1];
        myLib.Load_Cookies_From_File(system.persist_cookies);
    } else if (parts[0] == '--output') {
        system.result_dir = parts[1];
        //myLib.checkDirectory(system.result_dir);
    } else if (parts[0] == '--user-agent') {
        page.settings.userAgent = myLib.get_useragent(parts[1]);
    }
});


// locate the right type of store
if (service == 'cars') {
  store_list = cars.store_list;
  store_map = cars.store_map;
}
else if (service == 'hotels') {
  store_list = hotels.store_list;
  store_map = hotels.store_map;
}
else if (service == 'ecommerce') {
  store_list = ecommerce.store_list;
  store_map = ecommerce.store_map;
}
else {
  myLib.log("Unknown service: " + service);
  phantom.exit();
}

if (store_list.indexOf(store) == -1) {
  myLib.log("Unknown store: " + store);
  phantom.exit();
}
store = store_map[store];
for (item in store.searches) system.search_terms.push(item);

function save_results() {
    // Too many sites redirect or add parameters to the URL for this check to be reliable
    /*
    if (!store.dont_check_url && page.url != decodeURIComponent(store.searches[system.search_terms[system.search_index]])) {
        system.errors += 1;
        if (system.errors > system.MAX_ERRORS) {
            if (system.persist_cookies) myLib.Save_Cookies_To_File(system.persist_cookies);
            phantom.exit();
        }

        if (system.clear_cookies) phantom.clearCookies();

        console.log(page.url);
        console.log(decodeURIComponent(store.searches[system.search_terms[system.search_index]]));
        console.log('Retrying search for ' + system.search_terms[system.search_index]);
        page.open(store.searches[system.search_terms[system.search_index]]);
        setTimeout(save_results, system.PAGE_LOAD_WAIT);
        return;
    }
    */

    var fileName = system.result_dir + '/' + system.search_terms[system.search_index];
    system.errors = 0;
    console.log('Retrieved ' + system.search_terms[system.search_index]);
    myLib.save_page(fileName);

    setTimeout(search, system.SEARCH_WAIT);
}

function search() {
    if (system.clear_cookies) phantom.clearCookies();

    system.search_index += 1;
    if (system.search_index == system.search_terms.length) {
        if (system.persist_cookies) myLib.Save_Cookies_To_File(system.persist_cookies);
        phantom.exit();
    }

    console.log('Searching for ' + system.search_terms[system.search_index]);
    page.open(store.searches[system.search_terms[system.search_index]]);
    setTimeout(save_results, system.PAGE_LOAD_WAIT);
}

function login_start() {
    console.log("Clicking the login button");
    myLib.click_selector(store.login_button_selector);
    setTimeout(login, system.PAGE_LOAD_WAIT);
}

function login() {
    myLib.log("Logging in");

    if (store.framebust) {
	if (store.name == "sears") { // horrendous hack for sears' moving login form
	    store.frame_id = page.evaluate(function() { return document.querySelector('#modalIframe').firstElementChild.id; });
	    console.log("----------------> " + store.frame_id);
	}

	page.evaluate(function(frame, user, pass, user_selector, pass_selector) {
            window.frames[frame].document.querySelector(user_selector).value = user;
            window.frames[frame].document.querySelector(pass_selector).value = pass;
	}, store.frame_id, system.username, system.password,
		      store.username_selector, store.password_selector);
	myLib.save_page(system.result_dir + '/' + "login_pre");
	myLib.click_selector_in_frame(store.frame_id, store.login_submit_selector);
    }
    else {
	page.evaluate(function(user, pass, user_selector, pass_selector) {
            document.querySelector(user_selector).value = user;
            document.querySelector(pass_selector).value = pass;
	}, system.username, system.password, store.username_selector, store.password_selector);
	myLib.save_page(system.result_dir + '/' + "login_pre");
	myLib.click_selector(store.login_submit_selector);
    }

    setTimeout(login_finish, system.PAGE_LOAD_WAIT);
}

function login_finish() {
    console.log("Done with login, starting searches");
    myLib.save_page(system.result_dir + '/' + "login_post");
    page.open(store.url);
    setTimeout(search, system.PAGE_LOAD_WAIT);
}

setTimeout(function() {
    console.log('Browsing to ' + store.url);
    page.open(store.url);
    if (system.login) setTimeout(login_start, system.PAGE_LOAD_WAIT);
    else setTimeout(search, system.PAGE_LOAD_WAIT);
}, system.INITIAL_WAIT);

