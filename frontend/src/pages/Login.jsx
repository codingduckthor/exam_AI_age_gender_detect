import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

import "./Login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (token) {
      navigate("/home");
    }
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      setError("");

      const response = await axios.post("http://localhost:8000/login", {
        email,
        password,
      });

      if (!response.data.success) {
        setError(response.data.message);
        return;
      }

      localStorage.setItem("token", response.data.token);

      localStorage.setItem("username", response.data.username);

      navigate("/home");
    } catch (err) {
      console.error(err);

      setError(err.response?.data?.message || "Ошибка входа");
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <h2>Вход</h2>

        <form className="login-form" onSubmit={handleLogin}>
          <div>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div>
            <input
              type="password"
              placeholder="Пароль"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button className="login-btn" type="submit">
            Войти
          </button>
        </form>

        <br />

        <button className="register-btn" onClick={() => navigate("/register")}>
          Регистрация
        </button>

        {error && <p className="error">{error}</p>}
      </div>
    </div>
  );
}

export default Login;
