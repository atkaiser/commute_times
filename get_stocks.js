const puppeteer = require('puppeteer');

async function get_sandp() {
  var result = "";
  const browser = await puppeteer.launch({
    userDataDir: './cached-data',
//    headless: false
  });
  try {
    const page = await browser.newPage();
    await page.setViewport({
      width: 1920,
      height: 1080
    });

    await page.goto("https://www.thestreet.com/");
    const main_element = await page.waitForXPath(
      '//phoenix-tab[@for="^GSPC"]',
      {visible: true}
    );
    const classes = await (await main_element.getProperty('className')).jsonValue();
    const is_down = classes.includes("is-down");
    const price_element = await page.waitForXPath(
      '//phoenix-tab[@for="^GSPC"]//div[@class="m-market-data-index--current-price"]',
      {visible: true}
    );
    current_price = await (await price_element.getProperty('innerText')).jsonValue();

    const change_element = await page.waitForXPath(
      '//phoenix-tab[@for="^GSPC"]//div[@class="m-market-data-index--change"]',
      {visible: true}
    );
    current_change = await (await change_element.getProperty('innerText')).jsonValue();

    result = construct_result(current_price, current_change, is_down);

  } catch (error) {
    console.log(error);
  }

  await browser.close();
  return result;
}

function construct_result(current_price, current_change, is_down) {
  var correct_change = current_change;
  if (is_down) {
    correct_change = "-" + current_change;
    var first_paren = correct_change.indexOf("(");
    correct_change =
      correct_change.substring(0, first_paren + 1) +
      "-" +
      correct_change.substring(first_paren + 1, correct_change.length);
  }
  var result = current_price + " " + correct_change;
  result = result.substring(0, result.length - 1) + "%)";
  return result;
}

module.exports = {
  get_sandp
};
