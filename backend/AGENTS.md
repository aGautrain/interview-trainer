## Dev environment tips

- To build use `docker-compose build`.
- To deploy after building run `docker-compose up -d`.

## Testing instructions

- Run `docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit` to run every check in tests folder.
