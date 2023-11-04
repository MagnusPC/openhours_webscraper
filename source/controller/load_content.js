function waitCss(selector, n=1, require=false, timeout=5000) {
    console.log(selector, n, require, timeout);
    const start = Date.now();
    while (Date.now() - start < timeout) {
        if (document.querySelectorAll(selector).length >= n) {
            return document.querySelectorAll(selector);
        }
    }
    if (require) {
        throw new Error(`selector "${selector}" timed out in ${Date.now() - start} ms`);
    } else {
        return document.querySelectorAll(selector);
    }
}
const results = waitCss("div[role*=article]>a", n = 10, require = false);
// return Array.from(results).map((el) => el.getAttribute("href"))