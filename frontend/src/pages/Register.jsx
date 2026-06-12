import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import "./Register.css";

function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://localhost:8000/register", {
        username: form.username,
        email: form.email,
        password: form.password,
      });

      if (!response.data.success) {
        alert(response.data.message);
        return;
      }

      // после регистрации делаем login автоматически
      const loginResponse = await axios.post("http://localhost:8000/login", {
        email: form.email,
        password: form.password,
      });

      localStorage.setItem("token", loginResponse.data.token);
      localStorage.setItem("username", loginResponse.data.username);

      navigate("/home");
    } catch (err) {
      console.error(err);
      alert("Register failed");
    }
  };

  return (
    <div className="register-page">
      <div className="register-card">
        <h1>Register</h1>

        <form className="register-form" onSubmit={handleRegister}>
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={form.username}
            onChange={handleChange}
          />

          <input
            type="email"
            name="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
          />

          <button type="submit">Create Account</button>
        </form>
      </div>
    </div>
  );
}

export default Register;
