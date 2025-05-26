<!-- ````markdown -->
# Little Lemon API

This project is a simple REST API for a restaurant management system called Little Lemon. It includes basic features for handling users, categories, menu items, carts, and orders.

## Features

- **User management**: Admin can create users and assign them roles like "Manager" and "Delivery Crew".
- **Categories and Menu Items**: Admin can create categories and menu items that can be featured.
- **Cart**: Customers can add items to their cart, specifying the quantity.
- **Order**: Customers can place orders, and delivery crew members can update order statuses.
- **Admin & Manager Access**: Managers can assign users to specific roles, and admins can create and manage menu items.

## Getting Started

### Prerequisites

- Python 3.8+
- Django 5.2+
- Django REST Framework
- SQLite or any other database
- Djoser for authentication (Token-based)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/little-lemon-api.git
<!-- ```` -->

2. Navigate into the project directory:

   ```bash
   cd little-lemon-api
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the migrations to set up the database:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser to manage the app:

   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

### API Endpoints

* **GET /api/categories/**: Get all categories.
* **POST /api/categories/**: Create a new category (Admin only).
* **GET /api/menu-items/**: Get all menu items.
* **POST /api/menu-items/**: Create a new menu item (Admin only).
* **GET /api/menu-items/{id}/**: Get details of a specific menu item.
* **POST /api/cart/**: Add items to the cart (Authenticated users only).
* **GET /api/cart/**: Get the current user's cart.
* **POST /api/orders/**: Place a new order (Authenticated users only).
* **GET /api/orders/**: Get all orders for the authenticated user or manager.
* **PATCH /api/orders/{id}/update/**: Update the status of an order (Delivery Crew only).

### Sample Data

To easily test the API, you can use the `data.json` file, which contains sample data for users, categories, menu items, carts, and orders.

### How to Use the Data File

1. Import the data into your database using the Django shell or custom management commands.

```bash
python manage.py shell
```

2. Load the JSON data (make sure your models are set up first):

```python
import json
from django.core.management import call_command

with open('data.json') as f:
    data = json.load(f)

# You can use this data to create users, categories, menu items, etc., programmatically.
```

Alternatively, you can use the Django admin to manually create and test the entities.

## Testing the API

To test the API endpoints, you can use tools like:

* **Postman**: For manual testing of individual endpoints.
* **Insomnia**: Another tool similar to Postman for API testing.
* **cURL**: Command line tool to interact with your API.

<!-- ## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. -->

```

### Key Points:
- The `README.md` provides a guide for setting up the project, starting the server, using the API, and testing with the sample data.
- The `data.json` file is structured for use in testing the API, containing sample users, categories, menu items, carts, and orders.
```
