import React, { useState, useEffect } from "react";
import axios from "axios";
import "./EmbryoAnalyzer.css";

const EmbryoAnalyzer = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    setSelectedFile(file);
    setPrediction(null);
    setConfidence(null);
    setErrorMessage(null);

    if (file) {
      setPreviewUrl(URL.createObjectURL(file));
    } else {
      setPreviewUrl(null);
    }
  };

  // Clean up the temporary image URL when it is no longer needed
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  const handleUpload = async () => {
    if (!selectedFile) {
      setErrorMessage("⚠️ Please select an image first.");
      return;
    }

    setLoading(true);
    setErrorMessage(null);

    const formData = new FormData();
    formData.append("image", selectedFile);

    const token = localStorage.getItem("token");

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/analyze",
        formData,
        {
          headers: {
            Authorization: token,
            "Content-Type": "multipart/form-data",
          },
        }
      );

      // Handle "Not an Embryo" case
      if (response.data.prediction === "Not an Embryo") {
        setPrediction("Invalid Image: Not an embryo ❌");
        setConfidence(0);
        return;
      }

      setPrediction(response.data.prediction);
      setConfidence(response.data.confidence);
    } catch (error) {
      console.error("Error uploading file: ", error);
      setErrorMessage(
        "❌ Error: Session expired or invalid image. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="card">

        <img
          src="https://thumbs.dreamstime.com/b/ivf-icon-background-graphic-web-design-simple-vector-sign-internet-concept-symbol-website-button-mobile-app-141017202.jpg"
          alt="IVF Analysis"
          className="banner"
        />

        <h1 className="title">Embryo Health Analyzer</h1>

        <p className="description">
          Upload an embryo image to analyze its health.
        </p>

        {/* File Upload */}
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="file-input"
        />

        {/* Embryo Image Preview */}
        {previewUrl && (
          <div className="image-preview">
            <img
              src={previewUrl}
              alt="Selected embryo"
            />
          </div>
        )}

        {/* Error Message */}
        {errorMessage && (
          <p className="error-message">
            {errorMessage}
          </p>
        )}

        {/* Analyze Button */}
        <button
          onClick={handleUpload}
          className="analyze-button"
          disabled={loading}
        >
          {loading ? (
            <>
              <span className="loader"></span> Analyzing...
            </>
          ) : (
            "Analyze"
          )}
        </button>

        {/* Result */}
        {prediction && (
          <div className="result">

            <p className="result-text">
              Prediction:{" "}
              <span
                className={
                  prediction.includes("Invalid") ? "error-text" : ""
                }
              >
                {prediction}
              </span>
            </p>

            {/* Suitable / Not Suitable Message */}
            {prediction === "Healthy" && (
              <p>✅ It is suitable for IVF</p>
            )}

            {prediction === "Unhealthy" && (
              <p>❌ It is not suitable for IVF</p>
            )}

            <p className="result-text">
              Confidence:{" "}
              <span>
                {confidence !== null ? confidence.toFixed(2) : "0.00"}
              </span>
            </p>

          </div>
        )}

      </div>
    </div>
  );
};

export default EmbryoAnalyzer;