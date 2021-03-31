> Write test cases which test the following actions/checks:
> - [x] check GET
> - [x] check POST
> - [x] check DELETE
> - [ ] check authentication
> - [x] check query parameters: mandatory, optional
> - [x] check schema

# Test cases


## `TC-1` The "GET album by id" request should return with status code 200
1. **Given** the {album_id} is added to the GET request
2. **When** the "GET album by id" request is sent
3. **Then** the response should contain status code 200

## `TC-2` The "GET album by id" response should contain the proper label and name
1. **Given** the {album_id} is added to the GET request
2. **When** the "GET album by id" request is sent
3. **Then** the response should contain the proper album label
4. **And** the response should contain the proper album name

## `TC-3` The "POST create playlist" request should return with status code 201
1. **Given** the {playlist_name} is added to the POST request's body
2. **And** the {playlist_desc} is added to the POST request's body
3. **And** the {playlist_is_public} is added to the POST request's body
4. **When** the "POST create playlist" request is sent
5. **Then**  the response should contain status code 201

## `TC-4` The "POST create playlist" response should contain the proper name, description and public properties
1. **Given** the {playlist_name} is added to the POST request's body
2. **And** the {playlist_desc} is added to the POST request's body
3. **And** the {playlist_is_public} is added to the POST request's body
4. **When** the "POST create playlist" request is sent
5. **Then** the response should contain the proper playlist name
6. **And** the response should contain the proper playlist description
7. **And** the response should contain the proper playlist public property

## `TC-5` The "POST add items to playlist" request should return with status code 201
1. **Given** the {playlist_id} is added to the POST request's body
2. **And** the {track_uris} is added to the POST request's body
3. **When** the "POST add items to playlist" request is sent
4. **Then** the response should contain status code 201

## `TC-6` The "POST add items to playlist" response should return with proper schema
1. **Given** the {playlist_id} is added to the POST request's body
2. **And** the {track_uris} is added to the POST request's body
3. **When** the "POST add items to playlist" request is sent
4. **Then** the response should be successfully validated against the corresponding schema defined in folder: schemas

## `TC-7` The "PUT update playlist details" request should return with status code 200
1. **Given** the {playlist_id} is added to the PUT request
2. **And** the {playlist_name} is added to the PUT request's body
3. **And** the {playlist_desc} is added to the PUT request's body
4. **And** the {playlist_is_public} is added to the PUT request's body
5. **When** the "PUT update playlist details" request is sent
6. **Then** the response should contain status code 200

## `TC-8` The "PUT update playlist details" request should change the name, description and visibility of the given playlist
1. **Given** the {playlist_id} is added to the PUT request
2. **And** the {playlist_name} is added to the PUT request's body
3. **And** the {playlist_desc} is added to the PUT request's body
4. **And** the {playlist_is_public} is added to the PUT request's body
5. **When** the "PUT update playlist details" request is sent
6. **Then** the name of the following playlist: {playlist_id} should be {playlist_name}
7. **And**  the desctiption of the following playlist: {playlist_id} should be {playlist_desc}
8. **And**  the visibility of the following playlist: {playlist_id} should be {playlist_is_public}