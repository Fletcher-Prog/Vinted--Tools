module.exports = exports = function(links, config) {
  var request = require('request');
  var now = require("performance-now");
  var sanitize = require("node-sanitize-options");
  config = sanitize.options(config, {
    name: "node-cron-link",
    time: 3, //every 3 minutes
    consoleLog: true,
    kickStart: false
  });
  if (!(links instanceof Array)) {
    if (links) {
      links = [links];
    } else {
      links = [];
    }
  }
  if (!links.length) {
    console.log(config.name + ": no link provided.");
    return false;
  }
  var setLink = function(link) {
    var time = link.time;
    delete link.time;
    var loop = function() {
      setTimeout(function() {
        call();
      }, time * 60 * 1000);
    };
    var call = function() {
      var startTime = now();
      if (config.consoleLog === true) {
        var date = new Date();
        if (config.consoleLog === true) console.log(config.name + ": " + date.toLocaleString() + ": calling link: " + link.url);
      }
      var method = "get";
      if (typeof link.form !== "undefined" || typeof link.formData !== "undefined") method = "post";
      request[method](link, (error, response, body) => {
        if (typeof link.callback === "undefined" && error) {
          console.log(error);
        }
        if (typeof link.callback !== "undefined") {
          link.callback(error, response, body);
        }
        if (config.consoleLog === true) console.log(config.name + ": " + date.toLocaleString() + ": " + link.url + ": done in " + (now() - startTime) + " millisecond(s).");
        loop();
      });
    };
    if (config.kickStart === true) call(); else loop();
  };
  for (var i=0; i<=links.length-1; i++) {
    var link = links[i];
    if (typeof link === 'string' || link instanceof String) {
      link = {url: link, time: config.time};
    }
    if (typeof link === 'object' && link !== null && typeof link.url !== "undefined") {
      if (typeof link.time === "undefined") link.time = config.time;
    }
    setLink(link);
  }
};