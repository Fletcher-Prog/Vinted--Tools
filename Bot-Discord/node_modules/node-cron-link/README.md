# node-cron-link
Call any link(s) at a set interval repeatedly. GET/POST

--------------------------------------------------

**Usage:**

```
var cronLink = require("node-cron-link");
cronLink(links, config);
```

links can be (check examples below):
- Single String
- Array of String(s)
- Single Object
- Array of Object(s)

config (default for all links):
- name: "node-cron-link" // any friendly name for console log.
- time: 3 // run every 3 minutes
- consoleLog: true // whether to log useful info in console.
- kickStart: false // if true will call links right away without waiting for set time.

------------------------------------------------------

**Example (Single link):**
```
var cronLink = require("node-cron-link");
cronLink("https://ipinfo.io/ip", {time: 2, kickStart: true}); //every 2 minutes
```

**Example (Single link, with options):**

```
var cronLink = require("node-cron-link");
cronLink({ // link as object
  url: "https://ipinfo.io/ip", // link to call
  time: 2, // call it every 2 minutes.
  callback: function(error, response, body) { // callback after link is called
    console.log(error, body);
  }
}, {kickStart: true});
```
- In the above example, please check that link is passed as an object. You can provide more request options to the link object like `json: true`. Please check more here: https://www.npmjs.com/package/request

**Example (Multiple links):**
```
var cronLink = require("node-cron-link");
cronLink(
  ["https://ipinfo.io/ip",
  "https://httpbin.org/get"],
  {time: 2, kickStart: true} // every 2 minutes in
);
```

**Example (Multiple links, with options):**
```
var cronLink = require("node-cron-link");
cronLink(
  [{ // link as object
    url: "https://ipinfo.io/ip", // link to call
    time: 2, // call it every 2 minutes.
    callback: function(error, response, body) { // callback after link is called
      console.log(error, body);
    }
  },
  { // link as object
    url: "https://httpbin.org/get", // json
    time: 5, // call it every 5 minutes.
    json: true,
    callback: function(error, response, body) { // callback after link is called
      console.log(error, body);
    }
  }],
  {kickStart: true}
);
```

**Example - Global config for all links:**
```
var cronLink = require("node-cron-link");
cronLink(
  [{ // link as object
    url: "https://ipinfo.io/ip", // link to call
    callback: function(error, response, body) { // callback after link is called
      console.log(error, body);
    }
  },
  { // link as object
    url: "https://httpbin.org/get", // json
    json: true,
    callback: function(error, response, body) { // callback after link is called
      console.log(error, body);
    }
  }],
  { //default config for all links
    name: "node-cron-link", // any friendly name for console log.
    time: 3, // run every 3 minutes
    consoleLog: true, // whether to log useful info in console.
    kickStart: true // if true will call links right away without waiting for set time.
  }
);
```

**Example - Same callback:**
```
var cronLink = require("node-cron-link");
var callback = function(error, response, body) { // callback after link is called
  console.log(error, body);
}
cronLink(
  [{ // link as object
    url: "https://ipinfo.io/ip", // link to call
    time: 2, // call it every 2 minutes.
    callback: callback
  },
  { // link as object
    url: "https://httpbin.org/get", // json
    time: 5, // call it every 5 minutes.
    json: true,
    callback: callback
  }],
  {kickStart: true}
);
```

**Example - POST:**
Just add the form OR formData with link object.
```
var cronLink = require("node-cron-link");
cronLink(
  [{ // link as object
    url: "https://httpbin.org/post", // link to call
    time: 2, // call it every 2 minutes.
    form: {this: "that", that: "this"},
    json: true,
    callback: function(error, response, body) { // callback after link is called
      console.log(error, body);
    }
  }],
  {kickStart: true}
);
```

------------------------------------------------

Check console log for the time it takes to call every link, and the time when the link was called. Default `consoleLog` is `true`.