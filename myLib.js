/* =================================================================================================
 * =================================================================================================
 * by: Arash Molavi Kakhki
 * 	   arash@ccs.neu.edu
 * 
 * Goal: this library contains all functions used in Mobile_vs_Desktop project 
 * =================================================================================================
 * =================================================================================================
 */

/*
 * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 * Variables
 * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 */
var DEBUG0 = 1;
var DEBUG1 = 1;
var iPhone_Safari = "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B146 Safari/8536.25";
var iPhone_Chrome = "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_2 like Mac OS X; en-us) AppleWebKit/536.26 (KHTML, like Gecko) CriOS/23.0.1271.100 Mobile/10B146 Safari/8536.25";
var Android_Chrome = "Mozilla/5.0 (Linux; Android 4.1.1; SCH-I535 Build/JRO03L) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19";

// Salt lake city
// var latitude = 40.762796;
// var longitude = -111.890945;

// Boston
// var latitude = 42.338903;
// var longitude = -71.093237;

/*
 * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 * Functions
 * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 */
function checkDirectory(dir) {
	//log(('checkDirectory: ' + dir));
	try {
		if (!fs.exists(dir))
			fs.makeDirectory(dir);
	} catch (error) {
		die_with_error("Could not create directory '" + dir + "': " + error);
	}
	if (!fs.isDirectory(dir))
		die_with_error("Could not create directory '" + dir
				+ "': Exists as a file.");
}
function die_with_error(message, fileName) {
	log('die_with_error: ' + message);
	page.render(('die_with_error' + fileName + '.png'));
	phantom.exit();
}
function log(msg) {
	console.log(msg);
}
function check_page(status) {
	if (DEBUG1)
		console.log('\tcheck_page');
	//if (status !== 'success')
	//	die_with_error("HTTP Problem, status=" + status);
		
    load_jq = page.evaluate(function() {
        if (typeof jQuery == 'undefined') return true;
        return false;
    });
		
	if (load_jq && !page.injectJs("jQuery-1.9.1.js"))
		die_with_error("Error injecting jQuery");
}
function save_page(fileName) {
	if (DEBUG1) log('save_page: ' + fileName);
	page.render(fileName + ".png");
	fs.write((fileName + ".html"), page.content, 'w');
	//if (exit) {
	//	var interval = setInterval(function() {
	//		clearInterval(interval);
	//		phantom.exit();
	//	}, 15000);
	//}
}
function next(func, callback) {
	if (DEBUG1)
		log(('next: ' + func));
	setTimeout(function() {
		page.onLoadFinished = callback;
		eval("function step() { " + func + " return 1; }");
		if (!page.evaluate(step))
			die_with_error("Unable to execute function '" + func + "'");
	}, 1000);
}
function next_click(theSelector, callback) {
	if (DEBUG1) log(('next_click: ' + theSelector));
	setTimeout(function() {
		page.onLoadFinished = callback;
        click_selector(theSelector);
	}, 1000);
}
function click_selector(theSelector) {
	if (DEBUG1)
		log('click_selector: ' + theSelector);
	
	console.log('Trying click on: ' + page.url);
	
	page.evaluate(function(selector) {
		function simulateMouseClick(selector) {
			var target = document.querySelectorAll(selector)[0];
			var myEvent = document.createEvent('MouseEvents');
			myEvent.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
			target.dispatchEvent(myEvent);
		};
		simulateMouseClick(selector);
	}, theSelector);
}
function click_selector_in_frame(frame, theSelector) {
    if (DEBUG1) log('click_selector: ' + theSelector);
	
    console.log('Trying click on: ' + page.url);
	
    page.evaluate(function(frame, selector) {
	function simulateMouseClick(frame, selector) {
	    var target = window.frames[frame].document.querySelectorAll(selector)[0];
	    var myEvent = window.frames[frame].document.createEvent('MouseEvents');
	    myEvent.initMouseEvent("click", true, true, window.frames[frame].window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
	    target.dispatchEvent(myEvent);
	};
	simulateMouseClick(frame, selector);
    }, frame, theSelector);
}
function getIP() {
	system.ip = page.evaluate(function() {
		return document.body.innerText;
	});
	if (DEBUG0)
		log(('getIP: ' + system.ip));
	system.fileNameSuffix += "ip_" + system.ip;
	system.afterIP();
}
function Load_Cookies_From_File(Path2File){
    log('Load_Cookies_From_File...');

    if (!fs.isFile(Path2File)) {
        log("Error: cookie file does not exist. Moving on...");
        return;
    }

    CookieJar = JSON.parse(fs.read(Path2File));
    for (var i = 0; i < CookieJar.length; i++) {
        JSONObject = CookieJar[i];
        phantom.addCookie(JSONObject);
    }
    log('Cookies Size: ' + phantom.cookies.length);
}
function Save_Cookies_To_File(Path2File) {
    log('Doing Save_Cookies_To_File...');
    log('CookieJar size: ' + phantom.cookies.length);
    f = fs.open(Path2File, "w");
    f.writeLine(JSON.stringify(phantom.cookies, null, 2));
    f.close();
}
function get_useragent(ua) {
    if (ua == 'default') return "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36";
    else if (ua == 'xp') return "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36";
    else if (ua == 'win7') return "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36";
    else if (ua == 'osx') return "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36";
    else if (ua == 'linux') return "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36";
    else if (ua == 'ie8') return "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)";
    else if (ua == 'chrome') return "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36";
    else if (ua == 'firefox') return "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0";
    else if (ua == 'safari') return "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25";
    // "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11a501 Safari/9537.53"
    else if (ua == 'safari_osx') return "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9) AppleWebKit/537.71 (KHTML, like Gecko) Version/7.0 Safari/537.71";
    else if (ua == 'android') return "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36";
    return '';
}

/* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 * Exported functions
 * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 */
exports.log = log;
exports.save_page = save_page;
exports.check_page = check_page;
exports.next = next;
exports.next_click = next_click;
exports.click_selector = click_selector;
exports.click_selector_in_frame = click_selector_in_frame;
exports.checkDirectory = checkDirectory;
exports.get_useragent = get_useragent;
exports.Load_Cookies_From_File = Load_Cookies_From_File;
exports.Save_Cookies_To_File = Save_Cookies_To_File;

