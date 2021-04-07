> Write test cases which test the following actions/checks:
> - [x] check GET
> - [x] check POST
> - [x] check DELETE
> - [x] check authentication
> - [x] check query parameters: mandatory, optional
> - [x] check schema

# Test cases

|ID|ACTC|Precondition|Actison(s)|Expected result(s)|
|---|---|---|---|---|
|TC-1|YEA|1. the {album_id} is added to the GET request|1. the "GET album by id" request is sent|1. the response should contain status code 200
|TC-2|YEA|1. the {album_id} is added to the GET request|1. the "GET album by id" request is sent|1. the response should contain the proper album label
|TC-3|YEA|1. the {album_id} is added to the GET request|1. the "GET album by id" request is sent|1. the response should contain the proper album name
|TC-4|YEA|1. the {OAUTH_TOKEN} is added to the GET request's header|1. the "GET current user profile" request is sent|1. the response should be successfully validated against the corresponding schema defined in folder: schemas

|TC-5|YEA|1. the {playlist_name} is added to the POST request's body<br>2. the {playlist_desc} is added to the POST request's body<br>3. the {playlist_is_public} is added to the POST request's body|1. the "POST create playlist" request is sent|1. the response should contain status code 201

|TC-6|YEA|1. the POST request's body does not contain the required field {playlist_name}|1. the "POST create playlist" request is sent|1. the response should contain status code 400

|TC-7|YEA|1. the {playlist_name} is added to the POST request's body<br>2. the {playlist_desc} is added to the POST request's body<br>3. the {playlist_is_public} is added to the POST request's body|1. the "POST create playlist" request is sent|1. the response should contain the proper playlist name

|TC-8|YEA|1. the {playlist_name} is added to the POST request's body<br>2. the {track_uris} is added to the POST request's body|1. the "POST add items to playlist" request is sent|1. the response should contain status code 201

|TC-9|YEA|1. the {playlist_name} is added to the POST request's body<br>2. the {track_uris} is added to the POST request's body|1. the "POST add items to playlist" request is sent|1. the response should be successfully validated against the corresponding schema defined in folder: schemas

|TC-10|YEA|1. the {playlist_id} is added to the PUT request<br>2. the {playlist_name} is added to the PUT request's body<br>3. the {playlist_desc} is added to the PUT request's body<br>4. the {playlist_is_public} is added to the PUT request's body|1. the "PUT update playlist details" request is sent|1. the response should contain status code 200

|TC-11|YEA|1. the {playlist_id} is added to the PUT request<br>2. the {playlist_name} is added to the PUT request's body|1. the "PUT update playlist details" request is sent|1. the name of the following playlist: {playlist_id} should be {playlist_name}

|TC-12|YEA|1. the {playlist_id} is added to the PUT request<br>2. the {playlist_desc} is added to the PUT request's body|1. the "PUT update playlist details" request is sent|1. the description of the following playlist: {playlist_id} should be {playlist_desc}

|TC-13|YEA|1. the {playlist_id} is added to the PUT request<br>2. the {is_playlist_public} is added to the PUT request's body|1. the "PUT update playlist details" request is sent|1. the visibility of the following playlist: {playlist_id} should be {is_playlist_public}

|TC-14|YEA|1. the {playlist_id} is added to the DELETE request|1. the "DELETE unfollow a playlist" request is sent|1. the response should contain status code 200