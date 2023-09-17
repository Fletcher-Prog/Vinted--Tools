exports.options = function(passedOptions, defaultOptions) {
  if (typeof passedOptions === "undefined") {
    return defaultOptions;
  } else {
    for (var key in defaultOptions) if (typeof passedOptions[key] === "undefined") passedOptions[key] = defaultOptions[key];
    return passedOptions;
  }
};