const puppeteer = require('puppeteer');

function delay(time) {
  return new Promise(function(resolve) { 
      setTimeout(resolve, time)
  });
}

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

    await page.goto("https://finance.yahoo.com/quote/%5EGSPC/");
    // const main_element = await page.waitForXPath(
    //   "//span[text() = 'SPIB']/../span[contains(@class, 'qmod-last')]"
    //   // {visible: true}
    // );
    // TODO: Fix this so it doesn't have to wait this long
    await delay(2000);

    const main_elements = await page.$x('//fin-streamer[@data-symbol="^GSPC"]');
    let current_price = 0;
    let current_change = 0;
    let change_percent = 0;
    for (let i = 0 ; i < main_elements.length ; i++) {
      const element = main_elements[i];
      const data_field = await page.evaluate(el => el.getAttribute("data-field"), element);
      let value = await page.evaluate(el => el.textContent, element);

      value = value.replace(/[A-Z]/g, '');
      value = value.replace(/,/g, '');
      value = value.replace(/\$/g, '');
      value = value.replace(/\+/g, '');

      if (data_field === "regularMarketPrice") {
        current_price = value;
      }
      if (data_field === "regularMarketChange") {
        current_change = value;
      }
      if (data_field === "regularMarketChangePercent") {
        change_percent = value;
      }
    }

    result = current_price + " " + current_change + change_percent;
  } catch (error) {
    console.log(error);
  }

  await browser.close();
  return result;
}

// Old code using thestreet.com that stopped working
// async function get_sandp() {
//   // Result should look like "2000.12 -23.32(-12.12%)" or
//   // if s and p is up:       "2000.12 23.32(12.12%)"
//   var result = "";
//   const browser = await puppeteer.launch({
//     userDataDir: './cached-data',
//     headless: true
//   });
//   try {
//     const page = await browser.newPage();
//     await page.setViewport({
//       width: 1920,
//       height: 1080
//     });

//     await page.goto("https://www.thestreet.com/");
//     const main_element = await page.waitForXPath(
//       "//span[text() = 'SPIB']/../span[contains(@class, 'qmod-last')]"
//       // {visible: true}
//     );

//     let value = await (await main_element.getProperty('innerText')).jsonValue();
//     // Result of this will look like: $3,900.86USD
//     value = value.replace(/[A-Z]/g, '');
//     value = value.replace(/,/g, '');
//     value = value.replace(/\$/g, '');
//     // console.log(value);


//     const change_element = await page.waitForXPath(
//       "//span[text() = 'SPIB']/../span[contains(@class, 'qmod-change-group')]"
//       // {visible: true}
//     );
//     const current_change = await (await change_element.getProperty('innerText')).jsonValue();
//     // Result of this will look like: -116.96(-2.91%)
//     // console.log(current_change);

//     result = value + " " + current_change;

//   } catch (error) {
//     console.log(error);
//   }

//   await browser.close();
//   return result;
// }

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
