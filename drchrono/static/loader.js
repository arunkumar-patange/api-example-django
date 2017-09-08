/*
 *
 */
// globals $, window, setTimeout, drchrono


var drchrono = drchrono || {};
(function ($) {
  $(document).ready(function () {
    // csrf setup
    $.ajaxSetup({headers: { 'X-CSRFToken': $('meta[name="csrf-token"]').attr('content') }});
    drchrono.init();
  });
})($);
