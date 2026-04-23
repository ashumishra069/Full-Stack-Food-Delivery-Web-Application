import React, { useState, useEffect } from "react";
import Login from "./login";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    localStorage.getItem("token") ? true : false
  );

  const [restaurants, setRestaurants] = useState([]);
  const [foods, setFoods] = useState([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);
  const [cart, setCart] = useState([]);

  useEffect(() => {
    if (isLoggedIn) fetchRestaurants();
  }, [isLoggedIn]);

  const fetchRestaurants = async () => {
    const res = await fetch("http://127.0.0.1:8000/restaurants");
    const data = await res.json();
    setRestaurants(data);
  };

  const fetchFoods = async (id) => {
    const res = await fetch(`http://127.0.0.1:8000/foods/${id}`);
    const data = await res.json();
    setFoods(data);
  };

  // 🛒 ADD TO CART
  const addToCart = (food) => {
    const existing = cart.find((item) => item.id === food.id);

    if (existing) {
      setCart(
        cart.map((item) =>
          item.id === food.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        )
      );
    } else {
      setCart([...cart, { ...food, quantity: 1 }]);
    }
  };

  // 🛒 PLACE ORDER
  const placeOrderFromCart = async () => {
    const token = localStorage.getItem("token");

    for (let item of cart) {
      await fetch("http://127.0.0.1:8000/orders", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          user_id: 1,
          food_id: item.id,
        }),
      });
    }

    alert("Order placed 🎉");
    setCart([]);
  };

  // 🔐 LOGIN CHECK
  if (!isLoggedIn) {
    return <Login setIsLoggedIn={setIsLoggedIn} />;
  }

  return (
    <div style={{ background: "#121212", color: "white", minHeight: "100vh" }}>
      
      {/* Navbar */}
      <div style={{ background: "#ff5722", padding: "15px", textAlign: "center" }}>
        🍕 QuickBite
      </div>

      <div style={{ maxWidth: "700px", margin: "20px auto" }}>

        {/* Restaurants */}
        <h2 style={{ color: "#ff9800" }}>🔥 Restaurants</h2>

        {restaurants.map((r) => (
          <div key={r.id} style={{ margin: "10px 0" }}>
            <button
              style={{
                width: "100%",
                padding: "10px",
                background:
                  selectedRestaurant?.id === r.id ? "#ff5722" : "#333",
                color: "white",
                border: "none",
              }}
              onClick={() => {
                setSelectedRestaurant(r);
                fetchFoods(r.id);
              }}
            >
              {r.name}
            </button>
          </div>
        ))}

        {/* Menu */}
        {selectedRestaurant && (
          <>
            <h2 style={{ color: "#ff9800" }}>
              🍽 {selectedRestaurant.name}
            </h2>

            {foods.map((f) => (
              <div
                key={f.id}
                style={{
                  background: "#1e1e1e",
                  padding: "10px",
                  margin: "10px 0",
                  display: "flex",
                  justifyContent: "space-between",
                }}
              >
                <span>
                  {f.name} — ₹{f.price}
                </span>

                <button onClick={() => addToCart(f)}>
                  Add 🛒
                </button>
              </div>
            ))}
          </>
        )}

        {/* CART */}
        <h2 style={{ color: "#ff9800" }}>🛒 Cart</h2>

        {cart.length === 0 && <p>No items</p>}

        {cart.map((item) => (
          <div key={item.id}>
            {item.name} x {item.quantity}
          </div>
        ))}

        {cart.length > 0 && (
          <button onClick={placeOrderFromCart}>
            Place Order 🎉
          </button>
        )}
      </div>
    </div>
  );
}

export default App;