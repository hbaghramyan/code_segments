## Code Share Application Specification

### Overview
Create an API service utilizing JSON and RESTful practices, purposed for the creation, dissemination, and management of code segments. This API should conform to the ensuing list of guidelines:

### Key Characteristics of a Code Segment
**2.1** The code portion has to include the code text and its associated programming language, with the options being Java, PHP, Python, JavaScript or Plain Text. There is also an opportunity to provide a title and author name but these are not mandatory.

### Timestamping
**2.2** Automatic timestamping should be in place to track the inception of each code segment.

### API Endpoints
**2.3** The API should maintain a single endpoint that enables the following capabilities:

- **2.3.1** Showcasing all the code segments. The API users can implement filters based on creation date or language and can also execute keyword searches within the title or content. It is essential to paginate the results, with each page defaulting to 20 entries and the upper limit capped at 100.
- **2.3.2** Introduction of new segments with the previously stated data. The response should include the JSON formatted new code segment in the body and the unique URL in the headers. Inclusion of a confidential secret in the response is also necessary for future deletion of the segment.
- **2.3.3** Retrieve a specific code segment using its unique ID.
- **2.3.4** Delete a particular code segment utilizing its unique ID and corresponding secret.
- **2.3.5** Any updates to a code segment should result in a fresh segment with a new ID and secret, instead of altering the existing segment.

### Accessibility
**2.4** The API should provide open access, permitting all actions to be carried out by anyone.

### Privacy
**2.5** The API should also provide a provision for private code segments. Such segments should be omitted from any list-based results, making them only reachable through their unique URL or ID.
