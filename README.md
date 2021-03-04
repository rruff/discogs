# discogs

A simple Python client for the [Discogs API](https://www.discogs.com/developers#page:home).

The intention is to allow me to work with my collection data in ways not exposed in the web site or the Discogs mobile app, e.g. filter by genres and media formats, etc.

For a Discogs client library that is already full-featured, see [python3-discogs-client](https://github.com/joalla/discogs_client).

## TODO
1. Use list comprehensions in `Client.list*` methods.
2. Add a model class for `Release`.
3. Implement `__len__` and `__getitem__` methods in Folders model class. 
