# Happy Holidays (backend)

## Deployed on:

- [Render](https://happy-holidays-backend.onrender.com/)

## Routes

| HTTP Method | Route               | Explanation                                              |
| ----------- | ------------------- | -------------------------------------------------------- |
| GET         | /                   | 'Hello, from Flask!'                                     |
| POST        | /register           | Register                                                 |
| POST        | /login              | Login                                                    |
| GET         | /logout             | Logout                                                   |
| GET         | /users              | List all users                                           |
| GET         | /users/:id          | Get user by id                                           |
| DELETE      | /users/:id          | Delete user by id                                        |
| GET         | /users/:name        | Get user by name                                         |
| DELETE      | /users/:name        | Delete user by name                                      |
| GET         | /users/:id/wants    | Get a specific user's wants                              |
| GET         | /users/:id/dislikes | Get a specific user's dislikes                           |
| GET         | /users/:id/dreams   | Get a specific user's dreams                             |
| GET         | /users/:id/wishlist | Get a specific user's wishlist (wants, dislikes, dreams) |
| GET         | /users/:id/friends  | Get a specific user's friends                            |
| POST        | /users/:id/friends  | Add a friend                                             |
| POST        | /share              | Email invite to application                              |
| GET         | /wants              | List all wants                                           |
| POST        | /wants              | Post a want                                              |
| GET         | /wants/:id          | Get want by id                                           |
| PUT         | /wants/:id          | Marks an item as purchased or unpurchased                |
| DELETE      | /wants/:id          | Delete want by id                                        |
| GET         | /dislikes           | List all dislikes                                        |
| POST        | /dislikes           | Post a dislike                                           |
| GET         | /dislikes/:id       | Get dislike by id                                        |
| DELETE      | /dislikes/:id       | Delete dislike by id                                     |
| GET         | /dreams             | List all dreams                                          |
| POST        | /dreams             | Post a dream                                             |
| GET         | /dreams/:id         | Get dream by id                                          |
| PUT         | /dreams/:id         | Marks an item as purchased or unpurchased                |
| DELETE      | /dreams/:id         | Delete dream by id                                       |

## Technologies

- Flask
- SQL
