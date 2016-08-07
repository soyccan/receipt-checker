'use strict';

const SELECT_SIZE = 6;
const ASK_REMOVE = '\n回不去囉，想好了嗎？';

/**
 * Check if receipt won lottery, for last 3 digits
 * @param {string} num Last 3 digits of receipt number
 * @param {Array.<string>} winNum Winning Numbers
 * @return {boolean} whether won or not
 */
function check(num, winNum) {
  if (/^\d{3}$/.test(num)) {
    return winNum.some(function(v) {
      return num == v.slice(-3);
    });
  } else {
    throw 'Require a 3-digit number';
  }
}

/**
 * Copy element, with given strings as text node
 * @param {Object} $elem jQuery element, original for copying
 * @param {Array.<string>} strings Text for each element
 * @return {Object} fragment that contains element copies
 */
function generate($elem, strings) {
  var frag = document.createDocumentFragment();
  strings.forEach(function(s) {
    $elem.clone(false).text(s).appendTo(frag);
  });
  return frag;
}


function getCustomWinNum() {
  return localStorage.customWinNum ?
      localStorage.customWinNum.split(',') : [];
}

function addCustomWinNum(value) {
  var a = getCustomWinNum();
  a.push(value);
  localStorage.customWinNum = a.join();
}

function delCustomWinNum(index) {
  var a = getCustomWinNum();
  a.splice(index, 1);
  localStorage.customWinNum = a.join();
}


function getRecord() {
  return localStorage.record ?
      localStorage.record.split(',') : [];
}

function addRecord(value) {
  var a = getRecord();
  a.push(value);
  localStorage.record = a.join();
}