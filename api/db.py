from databases import Database

DATABASE_URL = 'mysql://rohan:my-secret-pw@127.0.0.1:3306/articledb'

database = Database(DATABASE_URL)
