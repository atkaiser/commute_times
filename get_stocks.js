const puppeteer = require('puppeteer');

async function get_sandp() {
  // Result should look like "2000.12 -23.32(-12.12%)" or
  // if s and p is up:       "2000.12 23.32(12.12%)"
  var result = "";
  const browser = await puppeteer.launch({
    userDataDir: './cached-data',
    headless: true
  });
  try {
    const page = await browser.newPage();
    await page.setViewport({
      width: 1920,
      height: 1080
    });

    await page.goto("https://www.thestreet.com/");
    const main_element = await page.waitForXPath(
      "//span[text() = 'SPIB']/../span[contains(@class, 'qmod-last')]"
      // {visible: true}
    );

    let value = await (await main_element.getProperty('innerText')).jsonValue();
    // Result of this will look like: $3,900.86USD
    value = value.replace(/[A-Z]/g, '');
    value = value.replace(/,/g, '');
    value = value.replace(/\$/g, '');
    // console.log(value);


    const change_element = await page.waitForXPath(
      "//span[text() = 'SPIB']/../span[contains(@class, 'qmod-change-group')]"
      // {visible: true}
    );
    const current_change = await (await change_element.getProperty('innerText')).jsonValue();
    // Result of this will look like: -116.96(-2.91%)
    // console.log(current_change);

    result = value + " " + current_change;

  } catch (error) {
    console.log(error);
  }

  await browser.close();
  return result;
}

// function construct_result(current_price, current_change, is_down) {
//   // Result should look like "2000.12 -23.32(-12.12%)"
//   var correct_change = current_change;
//   if (is_down) {
//     correct_change = "-" + current_change;
//     var first_paren = correct_change.indexOf("(");
//     correct_change =
//       correct_change.substring(0, first_paren + 1) +
//       "-" +
//       correct_change.substring(first_paren + 1, correct_change.length);
//   }
//   var result = current_price + " " + correct_change;
//   result = result.substring(0, result.length - 1) + "%)";
//   return result;
// }

module.exports = {
  get_sandp
};
