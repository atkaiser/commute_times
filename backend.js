const puppeteer = require('puppeteer');

async function get_time(start, destination) {
  var time_str = "0";
  var summary_route_str = "";
  var route_details = [];
  const browser = await puppeteer.launch({
    userDataDir: './cached-data',
    headless: true,
  });
  try {
    const page = await browser.newPage();
    await page.setViewport({
      width: 1920,
      height: 1080
    });
    // await page.goto('http://maps.google.com/maps?f=q&source=s_q&hl=en&q=to+' + destination + '+from+' + start);
    const main_page_url = 'https://www.google.com/maps/dir/' + start + '/' + destination
    // console.log(main_page_url);
    await page.goto(main_page_url)
    const details_span = await page.waitForXPath('//span[text()="Details"]', {visible: true});
    const details_button = (await details_span.$x('..'))[0];
    details_button.click();
    // Old way of getting the info
    // const time_element = await page.waitForXPath("//h1[contains(@class, '-title')]");
    // const str = await (await time_element.getProperty('innerHTML')).jsonValue()
    // time_str = min_from_string(await (await time_element.getProperty('innerText')).jsonValue());
    // Get the whole page html and then search for the first time string which should be the total trip time
    const data = await page.evaluate(() => document.querySelector('*').outerHTML);
    const arr = [...data.matchAll(/(\d+ hr )?\d+ min</g)];
    time_str = min_from_string(arr[0][0]);
    const summary_route_element = await page.waitForXPath("//h1[@id='section-directions-trip-title-0']");
    summary_route_str = await (await summary_route_element.getProperty('innerText')).jsonValue();
    // const route_elements = await page.$x("//h2[contains(@class, 'directions-mode-group') and not(contains(@class, 'directions-mode-group-summary'))]");
    const route_elements = await page.$x("//h2[contains(@id, 'directions-mode-group')]");
    for (var i = 0; i < route_elements.length; i++) {
      var route_elem = route_elements[i];
      var raw_text = await (await route_elem.getProperty('innerText')).jsonValue();
      route_details.push(raw_text.split("\n")[0]);
    }
  } catch (error) {
    console.log(error);
  }

  await browser.close();
  return {'time': time_str, 'summary_route': summary_route_str, 'detailed_route': route_details.join("||")}
}

function min_from_string(time_str) {
  var hours = 0;
  const hour_regex = /(\d+) h/;
  var hour_match = time_str.match(hour_regex);
  if (hour_match) {
    hours = parseInt(hour_match[1]) * 60;
  }
  var minutes = 0;
  const min_regex = /(\d+) min/;
  var min_match = time_str.match(min_regex);
  if (min_match) {
    minutes = parseInt(min_match[1]);
  }
  return hours + minutes;
}

// Used to sleep during testing.
function delay(time) {
  return new Promise(function(resolve) { 
      setTimeout(resolve, time)
  });
}

module.exports = {
  get_time
};