CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL
);

INSERT INTO users (username, password, role) VALUES
('admin_user', '$2b$12$KIX7b2IlfF8.H0vY1q0vUuIQgH1B1K0CxF7T8J.mwhYaRYc/OQpE2', 'admin'),  -- password: admin123
('regular_user', '$2b$12$8s7Rbw8VqsfYoqRVqZc0FOg7k5VGnb8FfXNaeAIJeqFq0H3w1OTeW', 'user');   -- password: user123


CREATE TABLE IF NOT EXISTS recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    ingredients TEXT NOT NULL,
    steps TEXT NOT NULL,
    prep_time INT NOT NULL,
    difficulty VARCHAR(20) NOT NULL
);

INSERT INTO recipes (name, ingredients, steps, prep_time, difficulty) VALUES
('Spaghetti Carbonara', 'Spaghetti, bacon, eggs, Parmesan cheese, black pepper', 'Cook spaghetti. In a bowl, mix eggs and cheese. Cook bacon. Combine everything.', 20, 'easy'),
('Pancakes', 'Flour, milk, eggs, sugar, baking powder, salt', 'Mix dry ingredients. Add milk and eggs. Cook in a pan.', 15, 'easy'),
('Caesar Salad', 'Romaine lettuce, croutons, Parmesan, Caesar dressing', 'Chop lettuce. Mix with dressing, croutons, and cheese.', 10, 'easy'),
('Grilled Cheese Sandwich', 'Bread, cheese, butter', 'Butter bread, place cheese between slices. Grill until golden.', 10, 'easy'),
('Chicken Alfredo', 'Pasta, chicken, heavy cream, Parmesan cheese, garlic', 'Cook pasta and chicken. Make sauce with cream and cheese. Combine.', 25, 'medium'),
('Tomato Soup', 'Tomatoes, onion, garlic, vegetable broth, basil', 'Sauté onions and garlic. Add tomatoes and broth. Simmer and blend.', 30, 'easy'),
('French Toast', 'Bread, eggs, milk, cinnamon, sugar, vanilla extract', 'Mix eggs, milk, cinnamon, and vanilla. Dip bread, cook in a pan.', 15, 'easy'),
('Chicken Curry', 'Chicken, curry powder, coconut milk, onion, garlic', 'Cook onions and garlic. Add chicken and curry. Add coconut milk and simmer.', 40, 'medium'),
('Beef Tacos', 'Ground beef, taco seasoning, tortillas, lettuce, cheese, tomatoes', 'Cook beef with seasoning. Serve in tortillas with toppings.', 20, 'easy'),
('Vegetable Stir-fry', 'Broccoli, bell pepper, carrot, soy sauce, garlic, ginger', 'Cook vegetables with garlic and ginger. Add soy sauce and stir-fry.', 15, 'easy'),
('Lasagna', 'Lasagna noodles, ricotta cheese, mozzarella, Parmesan, ground beef, marinara sauce', 'Layer noodles, cheese, beef, and sauce. Bake until bubbly.', 60, 'medium'),
('Guacamole', 'Avocado, lime, salt, cilantro, onion, tomato', 'Mash avocado. Mix with lime, salt, and chopped ingredients.', 10, 'easy'),
('Chicken Parmesan', 'Chicken breast, Parmesan, mozzarella, marinara sauce, breadcrumbs', 'Bread and fry chicken. Top with cheese and sauce. Bake until melted.', 30, 'medium'),
('Scrambled Eggs', 'Eggs, milk, salt, pepper', 'Whisk eggs with milk, cook in a pan, stir gently.', 5, 'easy'),
('Beef Stew', 'Beef, potatoes, carrots, onion, beef broth, thyme', 'Brown beef. Add vegetables and broth. Simmer until tender.', 120, 'medium'),
('Chocolate Chip Cookies', 'Flour, sugar, brown sugar, butter, chocolate chips, eggs, baking soda', 'Mix ingredients, form cookies, bake.', 20, 'easy'),
('Chicken Noodle Soup', 'Chicken, noodles, carrots, celery, onion, chicken broth', 'Cook chicken and vegetables in broth. Add noodles and cook until tender.', 40, 'easy'),
('Fried Rice', 'Rice, soy sauce, eggs, green onions, vegetables', 'Cook eggs, add rice and vegetables. Season with soy sauce.', 15, 'easy'),
('Garlic Bread', 'Bread, butter, garlic, parsley', 'Spread garlic butter on bread, bake until golden.', 10, 'easy'),
('Potato Salad', 'Potatoes, mayonnaise, mustard, celery, onion', 'Boil potatoes. Mix with other ingredients.', 25, 'easy'),
('BBQ Ribs', 'Pork ribs, BBQ sauce, salt, pepper', 'Season ribs, bake covered. Apply BBQ sauce, finish baking uncovered.', 180, 'medium'),
('Margarita Pizza', 'Pizza dough, tomato sauce, mozzarella, basil', 'Spread sauce on dough, top with cheese and basil. Bake.', 15, 'easy'),
('Shrimp Scampi', 'Shrimp, garlic, butter, lemon, parsley', 'Cook garlic in butter. Add shrimp and lemon juice. Garnish with parsley.', 10, 'easy'),
('Baked Salmon', 'Salmon, olive oil, lemon, garlic, herbs', 'Season salmon, bake until flaky.', 20, 'easy'),
('Eggplant Parmesan', 'Eggplant, marinara sauce, mozzarella, Parmesan, breadcrumbs', 'Bread and fry eggplant. Layer with cheese and sauce, bake.', 45, 'medium'),
('Clam Chowder', 'Clams, potatoes, onion, celery, heavy cream', 'Cook clams and vegetables in cream. Simmer until thick.', 40, 'medium'),
('Stuffed Peppers', 'Bell peppers, ground beef, rice, tomato sauce, cheese', 'Stuff peppers with beef and rice mixture, bake with sauce and cheese.', 50, 'medium'),
('Hummus', 'Chickpeas, tahini, olive oil, lemon, garlic', 'Blend all ingredients until smooth.', 10, 'easy'),
('Tuna Salad', 'Canned tuna, mayonnaise, celery, onion, salt, pepper', 'Mix all ingredients.', 5, 'easy'),
('Banana Bread', 'Bananas, flour, sugar, butter, eggs, baking soda', 'Mash bananas, mix with ingredients, bake.', 60, 'easy');
