## 1.3.5 (2023-11-26)

### Fix

- use PAT for commitizen push

## 1.3.4 (2023-11-26)

### Fix

- use correct path for count of user's groups

## 1.3.3 (2023-06-23)

### Fix

- CI use newer version for setup-python and actions-poetry

## 1.3.2 (2023-06-23)

### Fix

- update CI

## 1.3.1 (2023-03-17)

### Fix

- Update CI dependency

## 1.3.0 (2023-01-13)

### Feat

- `/attack-detection` endpoints (#7)

## 1.2.2 (2022-05-19)

### Fix

- remove unneeded ipython dev dependency

## 1.2.1 (2021-12-21)

### Fix

- update httpx to `^0.21`

## 1.2.0 (2021-12-21)

### Feat

- `/users/{user_id}/role-mappings/realm/composite` endpoint

## 1.1.1 (2021-11-26)

### Fix

- some typing issues resolved

## 1.1.0 (2021-11-19)

### Fix

- session related fixes
- linting configuration fixed

### Feat

- user-sessions for clients as well as sessions by id

## 1.0.3 (2021-11-09)

### Fix

- some typing issues fixed

## 1.0.2 (2021-11-08)

### Fix

- added readme field to pyproject.toml

## 1.0.1 (2021-11-08)

### Fix

- dummy commit to trigger version bump and pypi release

## 1.0.0 (2021-11-08)

### Refactor


- all uses off add replaced with create
- naming for type hints for Keycloak resource types changed
- moved introduction from index.rst to README.rst
- created separate module for httpx default args
- identified resources can be more cleanly chained

### BREAKING CHANGE

- The inconsistencies of using `add` or `create` have
been resolved in favor of `create`.
- Recursive data types like `GroupRepresentation` now work correctly and some missing fields have been added where they were missing.

### Fix

- will use refresh_token when it should and leeway configurable
- using __future__.annotations fix recursive representations
- user groups corretly returns list instead of a single
- correct behavior if no refresh_token is present

### Feat

- all currently implemented resources return id on creation
- execute-actions-email endpoints implemented
- incomplete groups resource
- create user function now returns the id of the created user
- incomplete authentication resource
- admin-events resource
- clients and default_client_scopes resources
- groups by user endpoints
- incomplete users resource
- grant_type=client_credentials flow allowed
- incomplete client-scopes resource
- incomplete implementation of the Roles resource
- wrapper architecture
