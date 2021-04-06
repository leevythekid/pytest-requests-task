> Write test cases which test the following actions/checks:
> - [x] check GET
> - [x] check POST
> - [x] check DELETE
> - [x] check authentication
> - [x] check query parameters: mandatory, optional
> - [x] check schema

# Test cases


## `TC-1` The "GET album by id" request should return with status code 200
1. **Given** the {album_id} is added to the GET request
2. **When** the "GET album by id" request is sent
3. **Then** the response should contain status code 200

## `TC-2` The "GET album by id" response should contain the proper label
1. **Given** the {album_id} is added to the GET request
2. **When** the "GET album by id" request is sent
3. **Then** the response should contain the proper album label

## `TC-3` The "GET album by id" response should contain the proper name
1. **Given** the {album_id} is added to the GET request
2. **When** the "GET album by id" request is sent
3. **Then** the response should contain the proper album name

## `TC-4` The "GET current user profile" response should return with proper schema
1. **Given** the {OAUTH_TOKEN} is added to the GET request's header
2. **When** the "GET current user profile" request is sent
3. **Then** the response should be successfully validated against the corresponding schema defined in folder: schemas

## `TC-5` The "POST create playlist" request should return with status code 201
1. **Given** the {playlist_name} is added to the POST request's body
2. **And** the {playlist_desc} is added to the POST request's body
3. **And** the {playlist_is_public} is added to the POST request's body
4. **When** the "POST create playlist" request is sent
5. **Then**  the response should contain status code 201

## `TC-6` The "POST create playlist" request should return with status code 400
1. **Given** the POST request's body does not contain the required field {playlist_name}
2. **When** the "POST create playlist" request is sent
3. **Then**  the response should contain status code 400

## `TC-7` The "POST create playlist" response should contain the proper name, description and public properties
1. **Given** the {playlist_name} is added to the POST request's body
2. **And** the {playlist_desc} is added to the POST request's body
3. **And** the {playlist_is_public} is added to the POST request's body
4. **When** the "POST create playlist" request is sent
5. **Then** the response should contain the proper playlist name
6. **And** the response should contain the proper playlist description
7. **And** the response should contain the proper playlist public property

## `TC-8` The "POST add items to playlist" request should return with status code 201
1. **Given** the {playlist_id} is added to the POST request's body
2. **And** the {track_uris} is added to the POST request's body
3. **When** the "POST add items to playlist" request is sent
4. **Then** the response should contain status code 201

## `TC-9` The "POST add items to playlist" response should return with proper schema
1. **Given** the {playlist_id} is added to the POST request's body
2. **And** the {track_uris} is added to the POST request's body
3. **When** the "POST add items to playlist" request is sent
4. **Then** the response should be successfully validated against the corresponding schema defined in folder: schemas

## `TC-10` The "PUT update playlist details" request should return with status code 200
1. **Given** the {playlist_id} is added to the PUT request
2. **And** the {playlist_name} is added to the PUT request's body
3. **And** the {playlist_desc} is added to the PUT request's body
4. **And** the {playlist_is_public} is added to the PUT request's body
5. **When** the "PUT update playlist details" request is sent
6. **Then** the response should contain status code 200

## `TC-11` The "PUT update playlist details" request should change the name of the given playlist
1. **Given** the {playlist_id} is added to the PUT request
2. **And** the {playlist_name} is added to the PUT request's body
3. **When** the "PUT update playlist details" request is sent
4. **Then** the name of the following playlist: {playlist_id} should be {playlist_name}

## `TC-12` The "PUT update playlist details" request should change the description of the given playlist
1. **Given** the {playlist_id} is added to the PUT request
2. **And** the {playlist_desc} is added to the PUT request's body
3. **When** the "PUT update playlist details" request is sent
4. **Then**  the description of the following playlist: {playlist_id} should be {playlist_desc}

## `TC-13` The "PUT update playlist details" request should change the visibility of the given playlist
1. **Given** the {playlist_id} is added to the PUT request
2. **And** the {is_playlist_public} is added to the PUT request's body
3. **When** the "PUT update playlist details" request is sent
4. **Then**  the visibility of the following playlist: {playlist_id} should be {is_playlist_public}

## `TC-14` The "DELETE unfollow a playlist" request should return with status code 200
1. **Given** the {playlist_id} is added to the DELETE request
2. **When** the "DELETE unfollow a playlist" request is sent
3. **Then** the response should contain status code 200