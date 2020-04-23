const puppeteer = require('puppeteer');

var my_args = process.argv.slice(2);
if (my_args.length != 2) {
  console.log("Run with node get_time.js start destination");
  process.exit(1);
}
const start = my_args[0];
const destination = my_args[1];

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({
    width: 1920,
    height: 1080
  });
  await page.goto('http://maps.google.com/maps?f=q&source=s_q&hl=en&q=to+' + destination + '+from+' + start);
  const details_span = await page.waitForXPath('//span[text()="Details"]');
  const details_button = (await details_span.$x('..'))[0];
  details_button.click();
  const time_element = await page.waitForXPath("//h1[@class='section-trip-summary-title']");
  const time_str = await (await time_element.getProperty('innerText')).jsonValue();
  console.log(time_str);
  const summary_route_element = await page.waitForXPath("//h1[@class='section-directions-trip-title']");
  const summary_route_str = await (await summary_route_element.getProperty('innerText')).jsonValue();
  const route_elements = await page.$x("//div[contains(@class, 'directions-mode-group') and not(contains(@class, 'directions-mode-group-summary'))]");
  console.log(summary_route_str);
  var route_details = [];
  for (var i = 0; i < route_elements.length; i++) {
    var route_elem = route_elements[i];
    var raw_text = await (await route_elem.getProperty('innerText')).jsonValue();
    route_details.push(raw_text.split("\n")[0]);
  }
  console.log(route_details);

  // wait 1 second
  // await new Promise((resolve, reject) => setTimeout(resolve, 1000));
  // '5024+Ray+Ave,+Castro+Valley,+CA+94546'
  // '777+Mariners+Island+Blvd,+San+Mateo,+CA+94404'

  await browser.close();
})();
