```
{
  _id: { x: "$message.guid"},
  message_id: {
    $last: "$_id"
  },
  message_text: {
    $last: "$message.text"
  },
  ids: {
    $addToSet: "$_id"
  }
}
```

Check the ids value and verify that all are same data

[Image](imgs/Screenshot 2020-03-03 at 10.10.12 PM.png)
[Image](imgs/Screenshot 2020-03-03 at 10.11.07 PM.png)

```
{
  _id: { x: "$message.guid"},
  message_id: {
    $first: "$_id"
  },
  message_text: {
    $last: "$message.text"
  },
  count: {
    $addToSet: "$_id"
  }
}
```

use $first

