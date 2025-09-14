ecommerce-project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   ├── cart.py
│   │   │   ├── order.py
│   │   │   └── otp.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   ├── cart.py
│   │   │   ├── order.py
│   │   │   └── otp.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py
│   │   │   ├── products/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py
│   │   │   ├── cart/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py
│   │   │   ├── checkout/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py
│   │   │   └── admin/
│   │   │       ├── __init__.py
│   │   │       └── routes.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   └── database.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── email.py
│   │   └── dependencies.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_main.py
│   ├── main.py
│   ├── seed.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.js
│   │   │   ├── Footer.js
│   │   │   ├── ProductCard.js
│   │   │   └── ProtectedRoute.js
│   │   ├── pages/
│   │   │   ├── Home.js
│   │   │   ├── Products.js
│   │   │   ├── ProductDetail.js
│   │   │   ├── Cart.js
│   │   │   ├── Checkout.js
│   │   │   ├── Success.js
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   └── Admin.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── context/
│   │   │   └── AuthContext.js
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   └── vite.config.js
└── README.md
