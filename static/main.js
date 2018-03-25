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



// refuse old IE
/*@cc_on
  @if (@_jscript_version < 9)
    window.location = 'unsupported.html';
  @end
@*/

$(function() {
  $('#mood, #mood-bad, #num-error, #add-error').hide();
  $('[title]').tooltip();

  $('#num-entry').keyup(function() {
    if ($('#num-entry').val().length >= 3) {
      var num = $('#num-entry').val();
      if (/^\d{3}$/.test(num)) {
        // match 3 digits
        if (check(num, winNum)) {
          $('#next-check').modal();
          $('#full-entry').focus();
        } else {
          $('#mood').hide();
          $('#mood-bad').show();
        }
        $('#result').text('這張是：' + num);
        $('#num-entry').parent().removeClass('has-error');
        $('#num-error').hide();
        addRecord(num);
      } else {
        $('#result').text('請輸入三位數');
        $('#num-entry').parent().addClass('has-error');
        $('#num-error').show();
      }
      $('#num-entry').val('');
    }
  });

  // TODO: focus on keyup

  $('#set-link').click(function() {
    $('#set-select').empty().attr('size',
        Math.max(SELECT_SIZE, getCustomWinNum().length));
    if (localStorage.customWinNum) {
      $('#set-select').append(
          generate($('<option>'), getCustomWinNum()));
    }
  });

  $('#history-link').click(function() {
    if (localStorage.record) {
      $('#record').empty().append(
          generate($('<li class="list-group-item">'), getRecord()));
      $('#history > i').hide();
      $('#history > div').show();
    } else {
      $('#record').empty();
      $('#history > i').show();
      $('#history > div').hide();
    }
  });

  $('#add').click(function() {
    // match 3 or 8 digits
    if (/^\d{3}(\d{5})?$/.test($('#add-entry').val())) {
      addCustomWinNum($('#add-entry').val());
      $('#set-link').click(); // refresh
      $('#add-entry').parent().removeClass('has-error');
      $('#add-error').hide();
    } else {
      $('#add-entry').parent().addClass('has-error');
      $('#add-error').show();
      alert('請輸入八位數或三位數');
    }
    $('#add-entry').val('');
  });

  $('#del').click(function() {
    // TODO: multiple delete
    if (confirm(
        '刪除：'
        + $('#set-select > :selected').text()
        + ASK_REMOVE)) {
      delCustomWinNum($('#set-select > :selected').index());
      $('#set-link').click(); // refresh
    }
  });

  $('#clear').click(function() {
    if (confirm('清空' + ASK_REMOVE)) {
      localStorage.customWinNum = '';
      $('#set-link').click(); // refresh
    }
  });

  $('#forget').click(function() {
    if (confirm('忘光' + ASK_REMOVE)) {
      localStorage.record = '';
      $('#history-link').click(); // refresh
    }
  });

  $('#ok').click(function() {
    if (/^\d{8}$/.test($('#full-entry').val())) {
      $.get(
        'full-check/',
        {
          'num': $('#full-entry').val(),
          'datecode': $('#date').val()
        },
        function(data) {
          if (data) {
            $('#result').html(
                '恭喜！你中了<strong>' + data.prizeName
                + '</strong>，獎金' + data.prizeValue + '元');
            $('#mood').show();
            $('#mood-bad').hide();
          } else {
            $('#result').text('真可惜，差一點就中了');
            $('#mood').hide();
            $('#mood-bad').show();
          }
        }
      );
      $('#next-check').modal('hide');
    } else {
      alert('請輸入八位數');
    }
  });

  $('#date').change(function() {
    if ($('#date').val() == 'custom') {
      winNum = getCustomWinNum();
    } else {
      $.get(
        'win-num/',
        { 'datecode' : $('#date').val() },
        function(data) { winNum = data; }
      );
    }
  });
});
