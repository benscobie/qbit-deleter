# Release Process

1. Update `CHANGELOG.md` with the version, date, and a summary.
2. Commit changes
    ```
    git commit -am "Prepare version vX.Y.Z"
    ```
3. Create annotated tag
    ```
    git tag -a vX.Y.Z -m 'Version vX.Y.Z'
    ```
4. Push commit and tag
    ```
    git push && git push --tags
    ```