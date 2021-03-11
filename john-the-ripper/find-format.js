/**
 * finds the regex in the .csv file
 * Usage:
 * a) node ./find-format.js
 * b) node ./find-format.js sha256
 */

const fs = require("fs");

const REGEX_FALLBACK = /md5/gi;

const pattern = process.argv.slice(2);
const REGEX = pattern[0] ? new RegExp(pattern, "gi") : REGEX_FALLBACK;

const formats = fs.readFileSync("./john-formats.csv").toString().split(",");

const matchingFormats = formats.filter((f) => REGEX.test(f));
matchingFormats.forEach((f) => console.log(f));
