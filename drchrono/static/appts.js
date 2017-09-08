/*
 *
 */
// globals $, window, setTimeout, moment, console

(function ($, window, setTimeout, moment) {
  $(document).ready(function () {

    // csrf setup
    $.ajaxSetup({headers: { 'X-CSRFToken': $('meta[name="csrf-token"]').attr('content') }});

    var formatdt = function (dt) {
      // return moment(dt).format("YYYY-MM-DD hh:mm A");
      return moment(dt).format("hh:mm A");
    };

    var apptHandler = function () {
      $('.appt-select', $('.appts')).change(function () {
          // update appt status
          clearTimeout(clearTimer);
          var _status = $("option:selected", $(this)).text();
          var _patient = $("option:selected", $(this)).val();
          var _token = $('meta[name="csrf-token"]').attr('content');
          // console.log(_status);
          // console.log(_patient);
          // $.post('/doctor/status/',
          $.ajax({
            url: '/doctor/appointments',
            method: 'put',
            data: {
              id: $(this).attr('data-appt-id'),
              status: _status,
              patient: _patient,
              csrfmiddlewaretoken:_token
            }
          })
          .done(function (data) {
            // console.log(data);
            clearTimer = setTimeout(poll, pollTime);
          });

      });
    }

    var getWaitTime = function (appt) {
        if (appt.status == "Arrived" && appt.arrived_at) {
            var now = moment(new Date());
            var diff = moment.duration(now.diff(moment(appt.arrived_at)));
            return diff.humanize() + " ago";
        }

        if (appt.status == "In Session" && appt.in_session_at) {
            var now = moment(new Date());
            var diff = moment.duration(now.diff(moment(appt.in_session_at)));
            return "for " + diff.humanize();
        }

        if (appt.status == "Complete") {
            var now = moment(appt.complete_at);
            var diff = moment.duration(now.diff(moment(appt.in_session_at)));
            return "in " + diff.humanize();
        }
    };

    var selects = function (appt, statuses) {
      var waitTime = getWaitTime(appt);
      var $sel = $("<select class='appt-select form-control'/>").attr('data-appt-id', appt.id);
      _.each(statuses, function (_status) {
          var text = waitTime && appt.status == _status ? _status + " ( " + waitTime + " ) " : _status
          var $opt = $("<option selected />").attr('value', appt.patient.id).text(text);
          $opt = _status == appt.status ? $opt : $opt.removeAttr("selected");
          $sel.append($opt);
      });
      return $sel;
    };

    var updateAppts = function (appts) {
        var $container = $('<div class="inline-div"/>');
        var $div = $(".appts-container").empty();
        _.each(appts.appts, function (appt, idx) {
          var $statusList = selects(appt, appts.statuses);
          var $name = $("<a/>").attr('href', "/patient/" + appt.patient.id)
                  .text(appt.patient.first_name + ' ' + appt.patient.last_name);

          $div.append(
            $("<div class='appts pull-left'/>").addClass(idx % 2 == 0 ? "top" : "bottom")
              .append($container.clone().append($name))
              .append($container.clone().text(" scheduled at " + formatdt(appt.scheduled_time)))
              .append($container.clone().append($statusList))
          );
        });
    }

    var pollTime = 1000 * 10;
    var poll = function () {
        $.get('/doctor/appointments', {format: 'json'})
          .done(function (data) {
            updateAppts(data);
            apptHandler();
            clearTimer = setTimeout(poll, pollTime);
          });
    }
    var clearTimer = setTimeout(poll, pollTime);
    apptHandler();
  });
})(
  $,
  window,
  setTimeout,
  moment
);
