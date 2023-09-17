# node-sanitize-options
Combines any options passed by user with default options so that they are never `undefined`.

Example:

```
var saveProduct = function(options) {
  var sanitize = require("node-sanitize-options");
  options = sanitize.options(options, {model: "ABC-001", price: 23.4, taxRate: 25, status: true});
  console.log(options);
};
saveProduct({model: "XYZ-002", price: 70.24});
```

will output:

```
{
  "model": "XYZ-002",
  "price": 70.24,
  "taxRate": 25,
  "status": true
}
```