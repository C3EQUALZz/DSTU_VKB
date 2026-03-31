import { useEffect, useState } from "react";

const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || "/api/v1").replace(/\/$/, "");
const healthUrl = import.meta.env.VITE_HEALTH_URL || "/health";

const emptyState = {
  label: "",
  confidence: 0,
  probabilities: {},
};

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [prediction, setPrediction] = useState(emptyState);
  const [serviceStatus, setServiceStatus] = useState("checking");
  const [isDragging, setIsDragging] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    let active = true;

    fetch(healthUrl)
      .then(async (response) => {
        if (!response.ok) {
          throw new Error("backend unavailable");
        }
        const payload = await response.json();
        if (active) {
          setServiceStatus(payload.status);
        }
      })
      .catch(() => {
        if (active) {
          setServiceStatus("offline");
        }
      });

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (!selectedFile) {
      setPreviewUrl("");
      return undefined;
    }

    const localPreview = URL.createObjectURL(selectedFile);
    setPreviewUrl(localPreview);

    return () => {
      URL.revokeObjectURL(localPreview);
    };
  }, [selectedFile]);

  function handleFileChange(file) {
    if (!file) {
      return;
    }

    setErrorMessage("");
    setPrediction(emptyState);
    setSelectedFile(file);
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (!selectedFile) {
      setErrorMessage("Сначала выбери изображение.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    setIsSubmitting(true);
    setErrorMessage("");

    try {
      const response = await fetch(`${apiBaseUrl}/predict`, {
        method: "POST",
        body: formData,
      });

      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Не удалось распознать изображение.");
      }

      setPrediction(payload);
    } catch (error) {
      setPrediction(emptyState);
      setErrorMessage(error.message || "Ошибка запроса.");
    } finally {
      setIsSubmitting(false);
    }
  }

  function onDrop(event) {
    event.preventDefault();
    setIsDragging(false);
    handleFileChange(event.dataTransfer.files?.[0] || null);
  }

  const rankedProbabilities = Object.entries(prediction.probabilities).sort((left, right) => right[1] - left[1]);

  return (
    <div className="app-shell">
      <div className="aurora aurora-left" />
      <div className="aurora aurora-right" />

      <main className="layout">
        <section className="hero-card">
          <div className="hero-header">
            <span className="eyebrow">Neural Figure Detector</span>
            <span className={`status-pill status-${serviceStatus}`}>{statusLabel(serviceStatus)}</span>
          </div>

          <h1>Shape Vision</h1>
          <p className="hero-copy">
            Загрузи изображение, а интерфейс покажет, какая геометрическая фигура на нём обнаружена и с какой уверенностью
            модель приняла решение.
          </p>

          <div className="shape-showcase" aria-hidden="true">
            <div className="shape-token circle-token" />
            <div className="shape-token triangle-token" />
            <div className="shape-token square-token" />
          </div>

          <div className="facts-grid">
            <article>
              <span>Classes</span>
              <strong>Circle / Triangle / Square</strong>
            </article>
            <article>
              <span>Flow</span>
              <strong>Upload -&gt; Predict -&gt; Confidence</strong>
            </article>
            <article>
              <span>Mode</span>
              <strong>FastAPI + React + Docker</strong>
            </article>
          </div>
        </section>

        <section className="panel-card">
          <form className="upload-form" onSubmit={handleSubmit}>
            <label
              className={`dropzone ${isDragging ? "dropzone-active" : ""} ${previewUrl ? "dropzone-has-image" : ""}`}
              onDragOver={(event) => {
                event.preventDefault();
                setIsDragging(true);
              }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={onDrop}
            >
              <input
                type="file"
                accept="image/*"
                onChange={(event) => handleFileChange(event.target.files?.[0] || null)}
              />

              {previewUrl ? (
                <div className="preview-frame">
                  <img src={previewUrl} alt="Предпросмотр загруженного изображения" className="preview-image" />
                </div>
              ) : (
                <div className="dropzone-copy">
                  <span className="dropzone-icon">▲</span>
                  <strong>Перетащи изображение сюда</strong>
                  <span>или нажми, чтобы выбрать файл</span>
                </div>
              )}
            </label>

            <div className="form-actions">
              <button type="submit" className="primary-button" disabled={isSubmitting}>
                {isSubmitting ? "Анализ..." : "Распознать фигуру"}
              </button>
              <p className="form-hint">Поддерживаются файлы, которые умеет читать Pillow: JPG, PNG и другие.</p>
            </div>
          </form>

          <section className="result-card">
            <div className="result-header">
              <span className="eyebrow">Result</span>
              {prediction.label ? <strong>{humanizeLabel(prediction.label)}</strong> : <strong>Ожидание запроса</strong>}
            </div>

            {errorMessage ? <p className="error-banner">{errorMessage}</p> : null}

            {prediction.label ? (
              <>
                <div className="confidence-meter">
                  <span>Уверенность модели</span>
                  <strong>{formatPercent(prediction.confidence)}</strong>
                </div>

                <div className="probability-list">
                  {rankedProbabilities.map(([label, probability]) => (
                    <div className="probability-row" key={label}>
                      <div className="probability-meta">
                        <span>{humanizeLabel(label)}</span>
                        <span>{formatPercent(probability)}</span>
                      </div>
                      <div className="probability-track">
                        <div className="probability-fill" style={{ width: `${probability * 100}%` }} />
                      </div>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <p className="placeholder-copy">
                После отправки изображения здесь появится итоговая фигура и распределение вероятностей по всем классам.
              </p>
            )}
          </section>
        </section>
      </main>
    </div>
  );
}

function humanizeLabel(label) {
  const dictionary = {
    circle: "Круг",
    triangle: "Треугольник",
    square: "Квадрат",
  };

  return dictionary[label] || label;
}

function statusLabel(status) {
  const dictionary = {
    checking: "checking",
    ready: "backend ready",
    model_missing: "training needed",
    offline: "backend offline",
  };

  return dictionary[status] || status;
}

function formatPercent(value) {
  return `${(value * 100).toFixed(1)}%`;
}

export default App;
