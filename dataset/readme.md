## JSON Data Structure Description

This JSON file contains a large collection (4000+) of Wikipedia navigation game session results.  
Each top-level key is a string identifier in the format:

```
FROM_<start_page>_TO_<end_page>
```

where `<start_page>` and `<end_page>` are Wikipedia page titles (with spaces replaced by underscores).

The value for each key is a list of player attempts for that specific navigation challenge.

Each player attempt is represented as an object with the following fields:

- **player_name**: *(string)*  
  The nickname of the player.

- **path_concept**: *(array of strings)*  
  The sequence of Wikipedia page titles that the player navigated through, starting from `<start_page>`.

- **won**: *(boolean)*  
  `true` if the player successfully reached the target page, `false` otherwise.

- **time**: *(integer or null)*  
  The time taken (in seconds) to complete the path, or `null` if not completed.

- **points**: *(integer or null)*  
  The points scored for the attempt, or `null` if not completed.

This structure allows for efficient storage and retrieval of multiple player attempts for many different start-to-end Wikipedia navigation challenges.

**Example:**
```json
{
  "FROM_Apple_TO_Banana": [
    {
      "player_name": "Alice",
      "path_concept": ["Apple", "Fruit", "Banana"],
      "won": true,
      "time": 45,
      "points": 100
    },
    {
      "player_name": "Bob",
      "path_concept": ["Apple", "Company", "Banana"],
      "won": false,
      "time": null,
      "points": null
    }
  ],
  "...": "..."
}
```
