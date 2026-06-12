import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import "./Home.css";
import Header from "../components/Header";

function Home() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const username = localStorage.getItem("username");

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/");
    }
  }, [navigate]);

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");

    navigate("/");
  };

  const uploadImage = async (e) => {
    try {
      const file = e.target.files[0];

      if (!file) return;

      if (!file.type.startsWith("image/")) {
        setError("Можно загружать только изображения");
        return;
      }

      setError("");

      const token = localStorage.getItem("token");

      if (!token) {
        navigate("/");
        return;
      }

      setImage(URL.createObjectURL(file));

      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post(
        "http://localhost:8000/predict",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      setResult(response.data);
    } catch (err) {
      console.error("Upload failed:", err);

      if (err.response?.status === 401) {
        localStorage.removeItem("token");
        localStorage.removeItem("username");

        navigate("/");

        return;
      }

      setError(err.response?.data?.message || "Ошибка обработки изображения");
    }
  };

  return (
    <>
      <Header username={username} />

      <div className="home-page">
        <div className="home-top">
          <h2>Возраст и пол по фотографии</h2>

          <button className="logout-btn" onClick={logout}>
            Выйти
          </button>
        </div>

        <div className="upload-box">
          <input
            className="upload-input"
            type="file"
            accept="image/*"
            onChange={uploadImage}
          />

          {error && <div className="error">{error}</div>}
        </div>

        <div className="result-grid">
          {image && (
            <div className="card">
              <h3>Загруженное изображение</h3>

              <img className="preview-image" src={image} alt="uploaded" />
            </div>
          )}

          {result?.image && (
            <div className="card">
              <h3>Обработанное изображение</h3>

              <img
                className="preview-image"
                src={`data:image/jpeg;base64,${result.image}`}
                alt="processed"
              />
            </div>
          )}

          {result?.faces?.length > 0 && (
            <div className="card">
              <h3>Результаты распознавания</h3>

              {result.faces.map((face, index) => (
                <div key={index} className="face-card">
                  <p>Возраст: {face.age}</p>

                  <p>
                    Точность возраста: {(face.age_confidence * 100).toFixed(2)}%
                  </p>

                  <p>Пол: {face.gender}</p>

                  <p>
                    Точность пола: {(face.gender_confidence * 100).toFixed(2)}%
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default Home;
