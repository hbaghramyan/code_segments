1. Design and implement a JSON-based RESTful API for creating and sharing code snippets. The API should meet the following requirements:
    1.1 A code snippet consists of a required text content which is the shared code and the language of that code, which should be a choice from Java, PHP, Python, JavaScript and Plain Text. Optionally it can have a title and an author name (freely chosen).
    1.2 For every code snippet the time creation should be tracked automatically.
    1.3 There should be one endpoint supporting the following actions:
        - Listing existing code snippets. Users of the API can filter by creation date or language, and they can search for keywords in title or content. The results should be paginated. The page size should be 20 by default and 100 at maximum.
        - Creating new snippets with the data mentioned above. The API should return the JSON representation of the newly created snippet in the body and its unique URL in the headers. Part of the response should be a secret that can be used for deleting the snippet.
        - Fetching a code snippet by its ID.
        - Deleting a code snippet by its ID and secret.
        - Updating a code snippet should yield a new snippet with a new ID and secret, rather than modifying the original one.
    1.4 The API should allow anonymous access, so anyone can perform any action.
    1.5 On the other hand, it should allow for private snippets. These should be excluded from list results, so they are only accessible by their direct URLs/IDs.

You can use any tech stack that you feel comfortable with, preferably Python, JavaScript, Java, C# or PHP.

Please don't upload the task or your created solutions anywhere where they can be accessed by the public.


